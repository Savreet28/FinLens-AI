import os

from dotenv import load_dotenv
from openai import OpenAI

# Read backend/.env and put its values into environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-5.4-mini"

CHROMA_DIR = "data/chroma"
COLLECTION_NAME = "financial_documents"
# Retrieval settings
TOP_K = 5            # how many chunks to retrieve for each question
MAX_DISTANCE = 0.75  # chunks farther than this are treated as "not relevant"


def get_openai_client():
    """Return an OpenAI client, or fail with a clear message if the key is missing."""
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to backend/.env")
    return OpenAI(api_key=OPENAI_API_KEY)