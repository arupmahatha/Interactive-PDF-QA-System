from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from app.services.pdf_service import PDFService
from app.services.embedding_service import EmbeddingService
from app.services.qa_service import QAService

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    chat_history: List[dict] = []

pdf_service = PDFService()
embedding_service = EmbeddingService()
qa_service = None

async def process_pdf(file_path: str):
    # Extract text from PDF
    documents = pdf_service.extract_text(file_path)
    
    # Create embeddings and initialize QA service
    embedding_service.create_embeddings(documents)
    global qa_service
    qa_service = QAService(embedding_service.vector_store)

async def generate_answer(question: str, chat_history: list):
    if not qa_service:
        raise HTTPException(status_code=400, detail="Please upload a PDF first")
    return await qa_service.generate_answer(question, chat_history)

@app.post("/upload")
async def upload_pdf(file: UploadFile):
    try:
        print(f"Received upload request for file: {file.filename}")  # Debug log
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        file_path = f"uploads/{file.filename}"
        print(f"Saving file to: {file_path}")  # Debug log
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        print("Processing PDF...")  # Debug log
        await process_pdf(file_path)
        
        return {"message": "File uploaded successfully"}
    except Exception as e:
        print(f"Error during upload: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))

# Add a basic health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        response = await generate_answer(request.question, request.chat_history)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 