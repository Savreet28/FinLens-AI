from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import DEMO_MODE, FRONTEND_URL
from app.routes import documents, research
from app.services.demo_service import index_demo_documents


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the server starts
    if DEMO_MODE:
        index_demo_documents()
    yield  # the server runs while we are "inside" this point


# Create the FastAPI application
app = FastAPI(title="FinLens-AI API", lifespan=lifespan)

# Only our own frontend may call this API from a browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(research.router)


@app.get("/")
def root():
    return {"message": "Welcome to the FinLens-AI API"}


@app.get("/api/health")
def health_check():
    return {"status": "ok", "demo_mode": DEMO_MODE}