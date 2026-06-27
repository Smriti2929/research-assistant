from fastapi import FastAPI
from pydantic import BaseModel

from app.services.gemini_service import ask_gemini

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