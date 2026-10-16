CHUNK_SIZE = 1000   # characters per chunk
CHUNK_OVERLAP = 200  # characters repeated between neighbouring chunks


def clean_text(text):
    """Collapse all whitespace (spaces, tabs, line breaks) into single spaces."""
    return " ".join(text.split())


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split one string into overlapping pieces of about chunk_size characters."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Don't cut a word in half: move the end back to the last space
        if end < len(text):
            last_space = text.rfind(" ", start, end)
            if last_space > start:
                end = last_space

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break  # reached the end of the text

                # Next chunk starts `overlap` characters before this one ended
        next_start = end - overlap

        # Don't start in the middle of a word: move forward to the next space
        next_space = text.find(" ", next_start, end)
        if next_space != -1:
            next_start = next_space + 1

        if next_start <= start:
            next_start = end  # safety: always move forward
        start = next_start

    return chunks


def chunk_pages(pages, document_name, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Turn [{"page": 1, "text": "..."}] into a list of chunks with metadata."""
    chunks = []

    for page in pages:
        page_text = clean_text(page["text"])
        pieces = split_text(page_text, chunk_size, overlap)

        for index, piece in enumerate(pieces):
            chunks.append({
                "id": f"{document_name}-p{page['page']}-c{index}",
                "text": piece,
                "metadata": {
                    "document": document_name,
                    "page": page["page"],
                    "chunk_index": index,
                },
            })

    return chunks