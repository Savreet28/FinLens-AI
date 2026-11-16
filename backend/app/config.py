import os

from dotenv import load_dotenv
from openai import OpenAI

# Read backend/.env and put its values into environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-5.4-mini"

CHROMA_DIR = os.getenv("CHROMA_DIR", "data/chroma")
COLLECTION_NAME = "financial_documents"
# Retrieval settings
TOP_K = 5            # how many chunks to retrieve for each question
MAX_DISTANCE = 0.75  # chunks farther than this are treated as "not relevant"

# Deployment settings (read from environment variables, with local defaults)
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
DEMO_DOCS_DIR = "demo_docs"
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
DAILY_QUESTION_LIMIT = int(os.getenv("DAILY_QUESTION_LIMIT", "200"))


def get_openai_client():
    """Return an OpenAI client, or fail with a clear message if the key is missing."""
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to backend/.env")
    return OpenAI(api_key=OPENAI_API_KEY)