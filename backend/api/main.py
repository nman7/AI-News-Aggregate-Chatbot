from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Setup config
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import FAISS_INDEX_FILE, METADATA_FILE, EMBEDDING_MODEL, GEN_MODEL_NAME

# ------------------ FASTAPI SETUP ------------------ #
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://0.0.0.0:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "News Highlights API is running."}

@app.get("/api/highlights")
def get_highlights():
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ------------------ LOAD MODELS ------------------ #
gen_model = None

try:
    faiss_index = faiss.read_index(FAISS_INDEX_FILE)
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    embed_model = SentenceTransformer(EMBEDDING_MODEL)

    tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(GEN_MODEL_NAME)
    gen_model = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

    print("✅ Models loaded successfully")

except Exception as e:
    print("❌ Failed to load models:", e)
    faiss_index, metadata, embed_model, gen_model = None, [], None, None

# ------------------ INPUT FORMAT ------------------ #
class ChatQuery(BaseModel):
    query: str
    top_k: int = 3

# ------------------ CHAT QUERY ENDPOINT ------------------ #
@app.post("/api/chat-query")
def chat_query(payload: ChatQuery):
    if not faiss_index:
        return {"error": "FAISS index not loaded properly."}

    if not embed_model:
        return {"error": "Embedding model not loaded properly."}

    if not gen_model:
        return {"error": "Generation model not loaded properly."}

    query_embedding = embed_model.encode([payload.query])[0].astype("float32")
    D, I = faiss_index.search(np.array([query_embedding]), payload.top_k)

    context = ""
    for idx in I[0]:
        if 0 <= idx < len(metadata):
            item = metadata[idx]
            summary = item.get("summary", "").strip()
            title = item.get("title", "").strip()
            category = item.get("category", "").strip().title()
            if summary:
                context += f"- ({category}) {title}: {summary}\n"

    prompt = f"You are a helpful assistant. Based on the news below, answer the following question.\n\nNews:\n{context}\n\nQuestion: {payload.query}\nAnswer:"

    try:
        result = gen_model(prompt, max_length=200)[0]["generated_text"].strip()
    except Exception as e:
        return {"error": f"Text generation failed: {e}"}

    return {
        "answer": result,
        "sources": [metadata[idx] for idx in I[0] if 0 <= idx < len(metadata)]
    }
