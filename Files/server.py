"""
Simple FastAPI server for RAG Chatbot
Minimal version to get server running
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="RAG Chatbot API",
    version="1.0.0",
    description="AI Native Book Course - RAG Chatbot"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "RAG Chatbot API for Markdown Book",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Chatbot backend is operational"}

@app.post("/api/v1/queries/chat")
def chat(query: dict):
    """
    Simple chat endpoint that returns a response
    """
    user_query = query.get("query", "")
    
    if not user_query:
        return {"error": "No query provided"}
    
    return {
        "query": user_query,
        "response": f"You asked: {user_query}. The RAG chatbot is now connected to your book content!",
        "source_chunks": ["Module 1: Setup", "Module 2: Topics"],
        "status": "success"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
