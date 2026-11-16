import shutil
import openai
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import DEMO_MODE
from app.services.pdf_service import extract_pages
from app.services.chunking_service import chunk_pages
from app.services.vector_store import list_documents, store_chunks
from app.errors import ai_error_to_http

router = APIRouter(prefix="/api/documents", tags=["documents"])

UPLOAD_DIR = Path("data/uploads")
MAX_FILE_SIZE_MB = 20


@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    # 0. The public demo does not accept uploads
    if DEMO_MODE:
        raise HTTPException(
            status_code=403,
            detail="Uploads are disabled in the live demo. Clone the repo to use your own documents.",
        )

    # 1. Only accept PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # 1b. Reject very large files (slow and expensive to embed)
    if file.size is not None and file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File is too large. Maximum size is {MAX_FILE_SIZE_MB} MB.",
        )

    # 2. Save the file to data/uploads/
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_name

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Extract text page by page
    try:
        pages = extract_pages(file_path)
    except ValueError as error:
        file_path.unlink(missing_ok=True)  # delete the bad file
        raise HTTPException(status_code=400, detail=str(error))

    # 4. Split the pages into overlapping chunks (stored in Phase 5)
    chunks = chunk_pages(pages, safe_name)

    # 5. Embed the chunks and store them in ChromaDB
    try:
        store_chunks(chunks)
    except (RuntimeError, openai.APIError) as error:
        raise ai_error_to_http(error)

    # 6. Return a short summary
    return {
        "document": safe_name,
        "pages_with_text": len(pages),
        "chunks": len(chunks),
        "characters": sum(len(p["text"]) for p in pages),
        "preview": pages[0]["text"][:300],
    }

@router.get("")
def get_documents():
    """List the documents that are already indexed in ChromaDB."""
    return list_documents()