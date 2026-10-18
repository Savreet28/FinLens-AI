from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import documents, research

# Create the FastAPI application
app = FastAPI(title="FinLens-AI API")

# Allow the React dev server to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the document routes (/api/documents/...)
app.include_router(documents.router)
app.include_router(research.router)


@app.get("/")
def root():
    return {"message": "Welcome to the FinLens-AI API"}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}