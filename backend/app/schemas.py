from pydantic import BaseModel, ConfigDict, Field


class ResearchRequest(BaseModel):
    """What React sends: {"question": "..."}"""
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(min_length=3, max_length=500)


class Source(BaseModel):
    """One piece of evidence from a document."""
    document: str
    page: int
    text: str
    distance: float


class ResearchResponse(BaseModel):
    """What FastAPI sends back."""
    answer: str
    sources: list[Source]