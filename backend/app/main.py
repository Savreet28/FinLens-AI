from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(title="FinLens-AI API")


@app.get("/")
def root():
    return {"message": "Welcome to the FinLens-AI API"}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}