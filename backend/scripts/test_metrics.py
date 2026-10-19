import sys

from app.services.metrics_service import extract_metrics
from app.services.vector_store import retrieve_relevant_chunks

question = sys.argv[1]
sources = retrieve_relevant_chunks(question)
print(f"Question: {question}")
print(f"Relevant chunks: {len(sources)}\n")

metrics = extract_metrics(question, sources) if sources else None

if metrics is None:
    print("No chart data (no metric with 2+ periods, or numbers failed verification).")
else:
    print(f"Metric: {metrics.metric_name} ({metrics.unit})")
    for point in metrics.points:
        print(f"  {point.period}: {point.value:,}")