import os
import chromadb
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

DATA_DIR = "data"
DB_DIR = "backend/db"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chroma_client = chromadb.PersistentClient(path=DB_DIR)
collection = chroma_client.get_or_create_collection(name="banking_docs")

chat_history = []


def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf(file_path):
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def create_vectorstore():
    os.makedirs(DATA_DIR, exist_ok=True)

    docs = []

    for file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, file)

        if file.endswith(".txt"):
            text = read_txt(file_path)
        elif file.endswith(".pdf"):
            text = read_pdf(file_path)
        else:
            continue

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"{file}_{i}",
                "text": chunk,
                "source": file
            })

    if not docs:
        return

    embeddings = embedding_model.encode([doc["text"] for doc in docs]).tolist()

    collection.upsert(
        ids=[doc["id"] for doc in docs],
        documents=[doc["text"] for doc in docs],
        embeddings=embeddings,
        metadatas=[{"source": doc["source"]} for doc in docs]
    )


def get_answer(question):
    question_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    context = "\n\n".join(results["documents"][0]) if results["documents"] else ""

    chat_history.append({"role": "user", "content": question})

    prompt = f"""
You are a helpful banking support chatbot.
Answer only using the given context.
If the answer is not available in the context, reply exactly: "The information is not available in the current dataset."

Context:
{context}

Conversation:
{chat_history[-6:]}

Question:
{question}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a factual banking support assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    chat_history.append({"role": "assistant", "content": answer})

    return answer