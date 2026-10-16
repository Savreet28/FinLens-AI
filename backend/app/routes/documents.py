import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.pdf_service import extract_pages
from app.services.chunking_service import chunk_pages

router = APIRouter(prefix="/api/documents", tags=["documents"])

UPLOAD_DIR = Path("data/uploads")


@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    # 1. Only accept PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

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

    # 5. Return a short summary
    return {
        "document": safe_name,
        "pages_with_text": len(pages),
        "chunks": len(chunks),
        "characters": sum(len(p["text"]) for p in pages),
        "preview": pages[0]["text"][:300],
    }