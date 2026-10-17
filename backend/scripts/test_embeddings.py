from app.config import EMBEDDING_MODEL, get_openai_client

sentences = [
    "The company's revenue grew strongly due to data center demand.",
    "Sales increased because of high demand for AI chips.",
    "The company's headquarters is located in Santa Clara, California.",
]

client = get_openai_client()
response = client.embeddings.create(model=EMBEDDING_MODEL, input=sentences)
vectors = [item.embedding for item in response.data]

print(f"Each embedding has {len(vectors[0])} numbers")
print(f"First 5 numbers of sentence 1: {vectors[0][:5]}")


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = sum(x * x for x in a) ** 0.5
    length_b = sum(y * y for y in b) ** 0.5
    return dot / (length_a * length_b)


print(f"\nSimilarity 1 vs 2 (same meaning, different words): {cosine_similarity(vectors[0], vectors[1]):.3f}")
print(f"Similarity 1 vs 3 (different topic):              {cosine_similarity(vectors[0], vectors[2]):.3f}")
print(f"\nTokens used: {response.usage.total_tokens}")