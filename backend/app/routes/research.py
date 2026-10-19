import openai
from fastapi import APIRouter, HTTPException

from app.errors import ai_error_to_http
from app.schemas import ResearchRequest, ResearchResponse
from app.services.vector_store import count_chunks, retrieve_relevant_chunks
from app.services.rag_service import extract_citations, generate_answer, is_insufficient
from app.services.metrics_service import extract_metrics

router = APIRouter(prefix="/api", tags=["research"])

NOT_FOUND_MESSAGE = (
    "I could not find enough relevant information in your uploaded "
    "documents to answer this question."
)


@router.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    # 1. There must be at least one indexed document
    if count_chunks() == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet. Please upload a PDF first.",
        )

    # 2. Retrieve the chunks that are close enough to the question
    try:
        sources = retrieve_relevant_chunks(request.question)
    except (RuntimeError, openai.APIError) as error:
        raise ai_error_to_http(error)

    # 3. Nothing relevant → say so honestly (no guessing)
    if not sources:
            return {"answer": NOT_FOUND_MESSAGE, "found": False, "sources": []}

    # 4. Generate a grounded answer from the evidence
    try:
        answer = generate_answer(request.question, sources)
    except (RuntimeError, openai.APIError) as error:
        raise ai_error_to_http(error)

        # 5. The LLM read the evidence but said it doesn't answer the question
    if is_insufficient(answer):
        return {"answer": answer, "found": False, "sources": []}

    # 6. Connect the answer to its sources:
    #    number them exactly as in the prompt, and mark which ones were cited
    cited_numbers = extract_citations(answer, len(sources))
    for number, source in enumerate(sources, start=1):
        source["number"] = number
        source["cited"] = number in cited_numbers

    # 7. Optional: structured numbers for a chart (never blocks the answer)
    try:
        metrics = extract_metrics(request.question, sources)
    except Exception as error:
        print(f"Metrics extraction failed: {error}")
        metrics = None

    return {"answer": answer, "found": True, "sources": sources, "metrics": metrics}