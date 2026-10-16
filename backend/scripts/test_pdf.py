import sys

from app.services.pdf_service import extract_pages

file_path = sys.argv[1]
pages = extract_pages(file_path)

total_chars = sum(len(p["text"]) for p in pages)
first = pages[0]

print(f"Pages with text: {len(pages)}")
print(f"Total characters: {total_chars}")
print(f"\n--- Page {first['page']} (first 500 characters) ---")
print(first["text"][:500])