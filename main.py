import os

from fastapi import FastAPI
from fastapi import File, UploadFile
from pydantic import BaseModel

from app.services.multi_document_service import (
    get_document_names
)
from app.utils.file_utils import save_chunks
from app.services.chunking_service import create_chunks
from app.services.gemini_service import ask_gemini
from app.services.pdf_service import extract_text_from_pdf
from app.services.embedding_service import get_embedding
from app.services.retrieval_service import load_chunks
from app.services.document_service import (
    get_uploaded_documents
)

from app.services.vector_service import(
    build_faiss_index,
    save_faiss_index,
    load_faiss_index,
    search_index
)

app = FastAPI(
    title= "Research Assistant",
    version= "1.0.0"
)

class ChatRequest(BaseModel):
    question: str

class AskRequest(BaseModel):
    file_name: str
    question: str

class MultiAskRequest(BaseModel):
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

@app.get("/documents")
def list_documents():

    documents = get_uploaded_documents()

    return {
        "documents": documents,
        "count": len(documents)
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

@app.post("/ask")
def ask_document(request: AskRequest):

    chunks = load_chunks(
        request.file_name
    )

    index = load_faiss_index(
        f"vectorstore/{request.file_name}.index"
    )

    question_embedding = get_embedding(
        request.question
    )

    chunk_indices = search_index(
        index,
        question_embedding
    )

    retrieved_chunks = []

    for idx in chunk_indices:

        if idx < len(chunks):
            retrieved_chunks.append(
                chunks[idx]
            )

    context = "\n\n".join(
        retrieved_chunks
    )

    prompt = f"""
You are a document research assistant.

Answer ONLY using the provided context. 

If the answer cannot be found in the context, say:

"I could not find that information in the document."

Context
{context}

Question:
{request.question}
"""
    
    answer = ask_gemini(
        prompt
    )

    return {
        "question": request.question,
        "answer": answer,
        "chunks_used": len(
            retrieved_chunks
        ),
        "sources": retrieved_chunks
    }

@app.post("/ask-all")
def ask_all_documents(
    request: MultiAskRequest
):
    
    documents = get_document_names()

    all_context = []

    question_embedding = get_embedding(
            request.question
    )

    for document in documents:

        chunks = load_chunks(
            document
        )

        index = load_faiss_index(
            f"vectorstore/{document}.index"
        )

        chunk_indices = search_index(
            index,
            question_embedding,
            top_k=2
        )

        for idx in chunk_indices:

            if idx < len(chunks):

                all_context.append(
                    f"DOCUMENT: {document}\n\n{chunks[idx]}"
                )

    context = "\n\n".join(
        all_context
    )

    prompt = f"""
You are a research assistant.

Answer using ONLY the context.

Context:
{context}

Question:
{request.question}
"""
    answer = ask_gemini(
        prompt
    )

    return {
        "question": request.question,
        "documents_searched": len(
            documents
        ),
        "answer": answer
    }
            