from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import os
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

# ------------------ FASTAPI SETUP ------------------ #
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ LOAD HIGHLIGHTS ------------------ #
@app.get("/api/highlights")
def get_highlights():
    with open("../scraper/news_data/combined_articles_with_summary_highlights.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def root():
    return {"message": "News Highlights API is running."}

# ------------------ EMBEDDING MODEL & FAISS ------------------ #
FAISS_INDEX_PATH = "../scraper/rag_index/highlight_index.faiss"
METADATA_PATH = "../scraper/news_data/combined_articles_with_summary_highlights.json"
EMBED_MODEL_PATH = "../scraper/highlights_model/all-MiniLM-L6-v2"
GEN_MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

try:
    faiss_index = faiss.read_index(FAISS_INDEX_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    embed_model = SentenceTransformer(EMBED_MODEL_PATH)

    # Load Mistral GGUF Model
    llm = Llama(
        model_path=GEN_MODEL_PATH,
        n_ctx=2048,
        n_threads=8,  # adjust per CPU
        use_mlock=True
    )
    print("✅ Models loaded successfully")

except Exception as e:
    print("❌ Failed to load models:", e)
    faiss_index, metadata, embed_model, llm = None, [], None, None

# ------------------ INPUT FORMAT ------------------ #
class ChatQuery(BaseModel):
    query: str
    top_k: int = 2

# ------------------ CHAT QUERY ENDPOINT ------------------ #
@app.post("/api/chat-query")
def chat_query(payload: ChatQuery):
    if not faiss_index or not embed_model or not llm:
        return {"error": "One or more models not loaded properly."}

    # Embed query and search
    query_embedding = embed_model.encode([payload.query])[0].astype("float32")
    D, I = faiss_index.search(np.array([query_embedding]), payload.top_k)

    # Prepare prompt pieces
    prompt_prefix = f"Answer the question: {payload.query}\n\nContext:\n"
    prompt_suffix = "\n\nAnswer:"
    max_ctx_tokens = 2048
    reserved_tokens_for_output = 400
    available_ctx_tokens = max_ctx_tokens - reserved_tokens_for_output

    # Build context dynamically based on token budget
    context = ""
    for idx in I[0]:
        if 0 <= idx < len(metadata):
            passage = metadata[idx]["raw_text"]
            temp_context = context + "\n\n" + passage
            full_prompt = prompt_prefix + temp_context + prompt_suffix
            token_count = len(llm.tokenize(full_prompt.encode("utf-8")))

            if token_count > available_ctx_tokens:
                break
            context = temp_context.strip()

    # Final safe prompt
    prompt = f"{prompt_prefix}{context}{prompt_suffix}"

    try:
        response = llm(prompt, max_tokens=400, stop=["</s>"])
        generated = response["choices"][0]["text"].strip()
    except Exception as e:
        return {"error": f"Text generation failed: {e}"}

    return {
        "answer": generated,
        "sources": [metadata[idx] for idx in I[0] if 0 <= idx < len(metadata)]
    }
