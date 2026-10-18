import sys

from app.services.rag_service import build_context, generate_answer
from app.services.vector_store import retrieve_relevant_chunks

question = sys.argv[1]
sources = retrieve_relevant_chunks(question)

print(f"Question: {question}")
print(f"Relevant chunks: {len(sources)}\n")

if not sources:
    print("No relevant evidence → the LLM is NOT called (no cost, no guessing).")
else:
    print("=== CONTEXT SENT TO THE LLM (first 800 characters) ===")
    print(build_context(sources)[:800], "...\n")
    print("=== ANSWER ===")
    print(generate_answer(question, sources))