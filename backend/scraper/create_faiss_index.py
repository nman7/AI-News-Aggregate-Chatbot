import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Config import
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import HIGHLIGHTS_JSON, FAISS_INDEX_FILE, METADATA_FILE, EMBEDDING_MODEL, RAG_INDEX_DIR

# Load model
model = SentenceTransformer(EMBEDDING_MODEL)

# Load highlights
with open(HIGHLIGHTS_JSON, "r", encoding="utf-8") as f:
    highlights = json.load(f)

print("-------------------------highlights", len(highlights))

# Prepare texts and metadata
texts = []
metadatas = []

for h in highlights:
    content = f"{h['title']} {h['summary']}"
    texts.append(content)
    metadatas.append({
        "title": h["title"],
        "summary": h["summary"],
        "url": h["url"],
        "category": h["category"],
        "sources": h["sources"],
        "frequency": h["frequency"]
    })

# Generate embeddings
embeddings = model.encode(texts, batch_size=16, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save index and metadata
os.makedirs(RAG_INDEX_DIR, exist_ok=True)
faiss.write_index(index, FAISS_INDEX_FILE)

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadatas, f, indent=2)

print(f"✅ FAISS index and metadata saved to {RAG_INDEX_DIR}")
