from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from backend.rag import create_vectorstore, get_answer

app = FastAPI(title="Banking RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "Banking chatbot backend is running"
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    create_vectorstore()

    return {
        "message": f"{file.filename} uploaded and indexed successfully"
    }


@app.post("/chat")
async def chat(query: dict):
    user_question = query.get("message", "")

    if not user_question.strip():
        return {
            "response": "Please enter a valid banking-related question."
        }

    answer = get_answer(user_question)

    return {
        "response": answer
    }