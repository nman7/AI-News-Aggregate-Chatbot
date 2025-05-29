import os
import json
from collections import Counter
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the local model
model = SentenceTransformer("models/all-MiniLM-L6-v2")

# Load articles
with open("data/combined_articles.json", "r", encoding="utf-8") as f:
    combined_data = json.load(f)

# Collect all articles
all_articles = []
for source, categories in combined_data.items():
    for category, articles in categories.items():
        for article in articles:
            title = article.get("title", "").strip()
            summary = article.get("summary", "").strip()
            raw_text = article.get("raw_text", "").strip()
            if not title:
                continue
            all_articles.append({
                "source": source,
                "category": category,
                "title": title,
                "summary": summary,
                "url": article["url"],
                "raw_text": raw_text
            })

print(f"✅ Total articles loaded: {len(all_articles)}")

# Generate embeddings from title + summary
texts = [a["title"] + " " + a["summary"] for a in all_articles]
embeddings = model.encode(texts, batch_size=16, show_progress_bar=True)

# Compute cosine similarity matrix
sim_matrix = cosine_similarity(embeddings)

# Cluster similar articles
THRESHOLD = 0.65
visited = set()
clusters = []

for i in range(len(all_articles)):
    if i in visited:
        continue
    cluster = [i]
    visited.add(i)
    for j in range(i + 1, len(all_articles)):
        if j not in visited and sim_matrix[i][j] > THRESHOLD:
            if all_articles[i]["source"] != all_articles[j]["source"]:
                cluster.append(j)
                visited.add(j)
    if len(cluster) > 1:
        clusters.append(cluster)

# Prepare highlights
highlight_data = []
for cluster in clusters:
    sources = [all_articles[i]["source"] for i in cluster]
    main_idx = cluster[0]
    highlight_data.append({
        "title": all_articles[main_idx]["title"],
        "summary": all_articles[main_idx]["summary"],
        "category": all_articles[main_idx]["category"],
        "url": all_articles[main_idx]["url"],
        "raw_text": all_articles[main_idx]["raw_text"],
        "sources": list(set(sources)),
        "frequency": len(cluster)
    })

# Save highlights
os.makedirs("data", exist_ok=True)
with open("data/highlights.json", "w", encoding="utf-8") as f:
    json.dump(highlight_data, f, indent=2)

print(f"📌 Highlights saved to data/highlights.json ({len(highlight_data)} items)")
