import sys
from pathlib import Path

from app.services.pdf_service import extract_pages
from app.services.chunking_service import chunk_pages
from app.services.vector_store import get_collection, store_chunks

file_path = sys.argv[1]
pages = extract_pages(file_path)
chunks = chunk_pages(pages, Path(file_path).name)

print(f"Embedding and storing {len(chunks)} chunks...")
store_chunks(chunks)

collection = get_collection()
print(f"Total records in ChromaDB: {collection.count()}")

# Read one record back to see exactly what was stored
record = collection.get(
    ids=[chunks[0]["id"]],
    include=["embeddings", "documents", "metadatas"],
)
print(f"\nRecord id: {record['ids'][0]}")
print("metadata: ", record["metadatas"][0])
print("text:     ", record["documents"][0][:200], "...")
print(f"embedding: {len(record['embeddings'][0])} numbers, starting with {record['embeddings'][0][:3]}")