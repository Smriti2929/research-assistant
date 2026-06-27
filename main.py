import os

from fastapi import FastAPI
from fastapi import File, UploadFile
from pydantic import BaseModel

from app.utils.file_utils import save_chunks
from app.services.chunking_service import create_chunks
from app.services.gemini_service import ask_gemini
from app.services.pdf_service import extract_text_from_pdf
from app.services.embedding_service import get_embedding

from app.services.vector_service import(
    build_faiss_index,
    save_faiss_index
)

app = FastAPI(
    title= "Research Assistant",
    version= "1.0.0"
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {
        "message": "Research Assistant API Running"
    }

@app.get("/health")
def health():
    return{
        "status": "healthy"
    }

@app.post("/chat")
def chat(request: ChatRequest):

    answer = ask_gemini(request.question)

    return {
        "question": request.question,
        "answer": answer
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return{
            "error": "Only PDF files are allowed"
        }

    os.makedirs("uploads", exist_ok= True)

    file_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)   

    pdf_data = extract_text_from_pdf(file_path)

    chunks = create_chunks(
        pdf_data["text"]
    )

    save_chunks(
        chunks,
        f"data/{file.filename}.json"
    )

    embeddings = []

    for chunk in chunks:
        embedding = get_embedding(chunk)
        embeddings.append(embedding)

    index = build_faiss_index(
        embeddings
    ) 

    save_faiss_index(
        index,
        f"vectorstore/{file.filename}.index"
    )   

    return {
        "filename": file.filename,
        "pages": pdf_data["pages"], 
        "characters": pdf_data["characters"],
        "chunks_created": len(chunks),
        "embeddings_created": len(embeddings)
    }     

