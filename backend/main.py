from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import os
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# ------------------ FASTAPI SETUP ------------------ #
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://ai-news-aggregate-chatbot.onrender.com"],  # Required for CORS
    allow_credentials=False,                  # Set to True only if using cookies/auth
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ EMBEDDING MODEL & FAISS ------------------ #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_INDEX_PATH = "scraper/rag_index/highlight_index.faiss"
METADATA_PATH = "scraper/news_data/combined_articles_with_summary_highlights.json"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
GEN_MODEL_NAME = "google/flan-t5-base"
# ------------------ LOAD HIGHLIGHTS ------------------ #
@app.get("/api/highlights")
def get_highlights():
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def root():
    return {"message": "News Highlights API is running."}

# ------------------ EMBEDDING MODEL & FAISS ------------------ #



gen_model = None

try:
    faiss_index = faiss.read_index(FAISS_INDEX_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    embed_model = SentenceTransformer(EMBED_MODEL_NAME)

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
    if not faiss_index or not embed_model or not gen_model:
        return {"error": "One or more models not loaded properly."}

    # 🔍 Step 1: Search similar news using FAISS
    query_embedding = embed_model.encode([payload.query])[0].astype("float32")
    D, I = faiss_index.search(np.array([query_embedding]), payload.top_k)

    # 🧠 Step 2: Build context with labeled summaries
    context = ""
    for idx in I[0]:
        if 0 <= idx < len(metadata):
            item = metadata[idx]
            summary = item.get("summary", "").strip()
            title = item.get("title", "").strip()
            category = item.get("category", "").strip().title()
            if summary:
                context += f"- ({category}) {title}: {summary}\n"

    # 📢 Step 3: Prepare prompt
    prompt = f"You are a helpful assistant. Based on the news below, answer the following question.\n\nNews:\n{context}\n\nQuestion: {payload.query}\nAnswer:"

    # 🧪 Step 4: Generate answer
    try:
        result = gen_model(prompt, max_length=200)[0]["generated_text"].strip()
    except Exception as e:
        return {"error": f"Text generation failed: {e}"}

    # ✅ Return result with related sources
    return {
        "answer": result,
        "sources": [metadata[idx] for idx in I[0] if 0 <= idx < len(metadata)]
    }
