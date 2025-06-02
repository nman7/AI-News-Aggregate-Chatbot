import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("models/all-MiniLM-L6-v2")

# Load highlights
with open("backend/data/highlights.json", "r", encoding="utf-8") as f:
    highlights = json.load(f)

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
os.makedirs("rag_index", exist_ok=True)
faiss.write_index(index, "rag_index/highlight_index.faiss")

with open("rag_index/metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadatas, f, indent=2)

print("✅ FAISS index and metadata saved to rag_index/")
