import openai
from fastapi import HTTPException


def ai_error_to_http(error):
    """Turn an OpenAI error (or a missing API key) into a clear HTTPException."""
    if isinstance(error, openai.AuthenticationError):
        return HTTPException(
            status_code=500,
            detail="OpenAI rejected the API key. Check OPENAI_API_KEY in backend/.env.",
        )
    if isinstance(error, openai.RateLimitError):
        return HTTPException(
            status_code=503,
            detail="OpenAI usage limit reached (no credits or too many requests). Try again later.",
        )
    if isinstance(error, openai.APIError):
        return HTTPException(
            status_code=502,
            detail="The AI service could not process the request. Please try again.",
        )
    # Anything else, e.g. RuntimeError("OPENAI_API_KEY is missing...")
    return HTTPException(status_code=500, detail=str(error))