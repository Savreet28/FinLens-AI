import pymupdf


def extract_pages(file_path):
    """Open a PDF and return its text page by page.

    Returns a list like: [{"page": 1, "text": "..."}, {"page": 2, "text": "..."}]
    Raises ValueError if the file is not a valid PDF or has no extractable text.
    """
    try:
        doc = pymupdf.open(file_path)
    except Exception:
        raise ValueError("This file could not be opened as a PDF.")

    pages = []
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:  # skip blank pages (e.g. pages with only images)
            pages.append({"page": page_number, "text": text})

    doc.close()

    if not pages:
        raise ValueError(
            "No extractable text found. The PDF may be a scanned image."
        )

    return pages