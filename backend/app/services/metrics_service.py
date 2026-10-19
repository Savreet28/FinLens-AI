from app.config import CHAT_MODEL, get_openai_client
from app.schemas import FinancialMetrics
from app.services.rag_service import build_context

METRICS_PROMPT = """You extract structured financial data from evidence.

If the evidence contains numeric values of ONE financial metric relevant to the
question, for at least two different periods (for example revenue for two quarters
or two years), return them. Otherwise set has_metrics to false and return an empty
points list.

Rules:
- Use only numbers written in the evidence. Never calculate, estimate or convert.
- Pick the single metric most relevant to the question.
- period: the period label as written in the evidence.
- value: the number exactly as written, without commas, currency symbols or units.
- unit: the unit as written (for example "$ in millions" or "%").
- List points in chronological order, oldest first."""


def number_appears(value, text):
    """Check that a number appears in the text, e.g. 30040.0 → "30,040" or "30040"."""
    value = abs(value)  # losses are often written as (1,234) in reports
    if value == int(value):
        variants = {f"{int(value):,}", str(int(value))}
    else:
        variants = {f"{value:,}", str(value), f"{value:,.2f}"}
    return any(variant in text for variant in variants)


def extract_metrics(question, sources):
    """Return verified FinancialMetrics for a chart, or None."""
    client = get_openai_client()

    response = client.chat.completions.parse(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": METRICS_PROMPT},
            {"role": "user", "content": f"Evidence:\n\n{build_context(sources)}\n\nQuestion: {question}"},
        ],
        response_format=FinancialMetrics,
    )
    metrics = response.choices[0].message.parsed

    # 1. The LLM found nothing chart-worthy
    if metrics is None or not metrics.has_metrics or len(metrics.points) < 2:
        return None

    # 2. Verify: every number must really appear in the evidence
    evidence_text = " ".join(source["text"] for source in sources)
    for point in metrics.points:
        if not number_appears(point.value, evidence_text):
            print(f"Metrics rejected: {point.value} not found in evidence")
            return None

    return metrics