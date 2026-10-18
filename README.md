# FinLens-AI -

AI Financial Research & Evidence Assistant — a document-grounded financial Q&A app built with RAG (Retrieval-Augmented Generation).

Upload financial PDFs, ask a question, and get an answer backed by evidence and page citations from your own documents.

**Stack:** React + Vite + Tailwind · FastAPI · PyMuPDF · OpenAI · ChromaDB

Work in progress — currently: backend skeleton + frontend layout (placeholder data).

how to run - 

cd /Users/savreetkaur28/FinLens-AI/backend
source venv/bin/activate
uvicorn app.main:app --reload

cd /Users/savreetkaur28/FinLens-AI/frontend
npm run dev