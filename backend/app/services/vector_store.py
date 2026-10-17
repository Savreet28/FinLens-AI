import chromadb

from app.config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL, get_openai_client

BATCH_SIZE = 100  # how many texts to send to OpenAI in one request

# Open (or create) the database files in data/chroma/
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)


def get_collection():
    """Return our collection, creating it the first time."""
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        configuration={"hnsw": {"space": "cosine"}},
        embedding_function=None,  # we create embeddings ourselves with OpenAI
    )


def embed_texts(texts):
    """Turn a list of strings into a list of embedding vectors."""
    client = get_openai_client()
    embeddings = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        embeddings.extend(item.embedding for item in response.data)

    return embeddings


def store_chunks(chunks):
    """Embed chunks and save them (vector + text + metadata) in ChromaDB."""
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts)

    collection = get_collection()
    collection.upsert(
        ids=[chunk["id"] for chunk in chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[chunk["metadata"] for chunk in chunks],
    )

    return len(chunks)

def search_chunks(question, top_k=5):
    """Find the top_k chunks whose meaning is closest to the question."""
    # 1. Turn the question into a vector (same model as the chunks!)
    question_embedding = embed_texts([question])[0]

    # 2. Ask ChromaDB for the nearest chunk vectors
    collection = get_collection()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
    )

    # 3. Chroma returns one inner list per question; we sent one question → [0]
    matches = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        matches.append({
            "text": text,
            "document": metadata["document"],
            "page": metadata["page"],
            "distance": round(distance, 3),
        })

    return matches