import sys

from app.services.vector_store import search_chunks

question = sys.argv[1]
top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

print(f'Question: "{question}"\n')

for rank, match in enumerate(search_chunks(question, top_k), start=1):
    print(f"#{rank}  distance={match['distance']}  |  {match['document']}  page {match['page']}")
    print(f"    {match['text'][:300]}...\n")