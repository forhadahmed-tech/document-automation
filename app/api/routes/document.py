from fastapi import APIRouter
from app.services.document_service import generate_documents

router = APIRouter()

@router.get("/generate-docs")
def generate_docs():
    files = generate_documents()
    return {"files": files}