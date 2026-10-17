import shutil
import openai
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.pdf_service import extract_pages
from app.services.chunking_service import chunk_pages
from app.services.vector_store import store_chunks

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

        # 5. Embed the chunks and store them in ChromaDB
    try:
        store_chunks(chunks)
    except RuntimeError as error:  # e.g. the API key is missing
        raise HTTPException(status_code=500, detail=str(error))
    except openai.AuthenticationError:
        raise HTTPException(
            status_code=500,
            detail="OpenAI rejected the API key. Check OPENAI_API_KEY in backend/.env.",
        )
    except openai.RateLimitError:
        raise HTTPException(
            status_code=503,
            detail="OpenAI usage limit reached (no credits or too many requests). Try again later.",
        )
    except openai.APIError:
        raise HTTPException(
            status_code=502,
            detail="The AI service could not process this document. Please try again.",
        )

    # 6. Return a short summary
    return {
        "document": safe_name,
        "pages_with_text": len(pages),
        "chunks": len(chunks),
        "characters": sum(len(p["text"]) for p in pages),
        "preview": pages[0]["text"][:300],
    }