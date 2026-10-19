from pydantic import BaseModel, ConfigDict, Field


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