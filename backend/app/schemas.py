from pydantic import BaseModel, ConfigDict, Field

class MetricPoint(BaseModel):
    """One value of a metric for one period."""
    period: str   # e.g. "Three months ended July 27, 2025"
    value: float  # e.g. 46743


class FinancialMetrics(BaseModel):
    """Structured numbers extracted from the evidence (used for the chart)."""
    has_metrics: bool
    metric_name: str          # e.g. "Revenue"
    unit: str                 # e.g. "$ in millions"
    points: list[MetricPoint]

class ResearchRequest(BaseModel):
    """What React sends: {"question": "..."}"""
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(min_length=3, max_length=500)


class Source(BaseModel):
    """One piece of evidence from a document."""
    number: int      # matches the [n] citation in the answer
    document: str
    page: int
    text: str
    distance: float
    cited: bool      # True if the answer cites this source


class ResearchResponse(BaseModel):
    """What FastAPI sends back."""
    answer: str
    found: bool      # False when the documents don't answer the question
    sources: list[Source]
    metrics: FinancialMetrics | None = None  # only when a chart makes sense