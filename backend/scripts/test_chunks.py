import sys
from pathlib import Path

from app.services.pdf_service import extract_pages
from app.services.chunking_service import chunk_pages

file_path = sys.argv[1]
chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
overlap = int(sys.argv[3]) if len(sys.argv) > 3 else 200

pages = extract_pages(file_path)
chunks = chunk_pages(pages, Path(file_path).name, chunk_size, overlap)

lengths = [len(c["text"]) for c in chunks]
print(f"Pages with text: {len(pages)}")
print(f"Chunks: {len(chunks)}  (size={chunk_size}, overlap={overlap})")
print(f"Average chunk length: {sum(lengths) // len(lengths)} characters")
print(f"Shortest: {min(lengths)}   Longest: {max(lengths)}")

# Find two neighbouring chunks from the same page to show the overlap
for i in range(1, len(chunks)):
    if chunks[i]["metadata"]["chunk_index"] == 1:
        first, second = chunks[i - 1], chunks[i]
        print(f"\n=== {first['id']} ===")
        print("metadata:", first["metadata"])
        print("...END OF CHUNK:", first["text"][-250:])
        print(f"\n=== {second['id']} ===")
        print("metadata:", second["metadata"])
        print("START OF CHUNK:", second["text"][:250], "...")
        break
else:
    print("\nNo page was long enough to produce 2 chunks.")