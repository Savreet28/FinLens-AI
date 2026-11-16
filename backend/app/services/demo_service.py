from pathlib import Path

from app.config import DEMO_DOCS_DIR
from app.services.chunking_service import chunk_pages
from app.services.pdf_service import extract_pages
from app.services.vector_store import list_documents, store_chunks


def index_demo_documents():
    """Index every PDF in demo_docs/ that is not already in ChromaDB."""
    already_indexed = {doc["document"] for doc in list_documents()}

    for pdf_path in sorted(Path(DEMO_DOCS_DIR).glob("*.pdf")):
        if pdf_path.name in already_indexed:
            continue  # skip it: no extra OpenAI cost

        pages = extract_pages(pdf_path)
        chunks = chunk_pages(pages, pdf_path.name)
        store_chunks(chunks)
        print(f"Demo document indexed: {pdf_path.name} ({len(chunks)} chunks)")