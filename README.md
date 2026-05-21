# 🏦 AI Banking Support Chatbot

An AI-powered Banking Support Chatbot built using FastAPI, Streamlit, ChromaDB, Sentence Transformers, and Groq LLM APIs.

The chatbot allows users to upload banking-related documents (TXT/PDF) and ask questions based on the uploaded dataset using Retrieval-Augmented Generation (RAG).

---

# 🚀 Features

- 📄 Upload TXT and PDF banking documents
- 🤖 AI-powered chatbot using Groq LLM
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic search using embeddings
- 💾 ChromaDB vector database integration
- ⚡ FastAPI backend
- 🎨 Streamlit frontend UI
- 📚 Context-aware document querying
- ⏳ Skeleton loading animation while AI responds
- 🚫 Handles unrelated questions gracefully

---

# 🛠️ Tech Stack

## Frontend
- Streamlit

## Backend
- FastAPI
- Python

## AI / NLP
- Groq API
- Sentence Transformers
- RAG Architecture

## Database
- ChromaDB (Vector Database)

---

# 📂 Project Structure

```bash
chatBot/
│
├── backend/
│   ├── app.py
│   ├── rag.py
│   └── db/
│
├── frontend/
│   └── streamlit_app.py
│
├── data/
│   ├── banking_support.txt
│   ├── credit_card_policy.txt
│   └── loan_faq.txt
│
├── uploads/
├── .env
├── requirements.txt
└── README.md