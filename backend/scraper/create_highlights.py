import os
import json
import re
import numpy as np
from collections import Counter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Config import
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import SUMMARY_JSON, HIGHLIGHTS_JSON, COSINE_THRESHOLD, EMBEDDING_MODEL

# Load model
model = SentenceTransformer(EMBEDDING_MODEL)

# Load articles
with open(SUMMARY_JSON, "r", encoding="utf-8") as f:
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
            })

print(f"✅ Total articles loaded: {len(all_articles)}")

# Generate embeddings
texts = [a["title"] + " " + a["summary"] for a in all_articles]
embeddings = model.encode(texts, batch_size=16, show_progress_bar=True)

# Compute similarity
sim_matrix = cosine_similarity(embeddings)

# Cluster similar articles
visited = set()
clusters = []

for i in range(len(all_articles)):
    if i in visited:
        continue
    cluster = [i]
    visited.add(i)
    for j in range(i + 1, len(all_articles)):
        if j not in visited and sim_matrix[i][j] > COSINE_THRESHOLD:
            if all_articles[i]["source"] != all_articles[j]["source"]:
                cluster.append(j)
                visited.add(j)
    if len(cluster) > 1:
        clusters.append(cluster)

# === Priority Keyword Highlights ===
priority_keywords = [
    "breaking", "exclusive", "alert", "just in", "urgent",
    "live", "update", "developing", "confirmed", "shocking"
]

def is_priority_article(article):
    title = article.get("title", "").lower()
    for kw in priority_keywords:
        if re.search(rf"\\b{re.escape(kw)}\\b", title):
            print(f"✅ Matched keyword: '{kw}' in title: '{title}'")
            return True
    return False

# Add cluster-based highlights
highlight_data = []
for cluster in clusters:
    sources = [all_articles[i]["source"] for i in cluster]
    main_idx = cluster[0]
    highlight_data.append({
        "title": all_articles[main_idx]["title"],
        "summary": all_articles[main_idx]["summary"],
        "category": all_articles[main_idx]["category"],
        "url": all_articles[main_idx]["url"],
        "sources": list(set(sources)),
        "frequency": len(cluster)
    })

# Add keyword-priority highlights
used_urls = {item["url"] for item in highlight_data}
for article in all_articles:
    if article["url"] not in used_urls and is_priority_article(article):
        print("--------------", article["title"])
        highlight_data.append({
            "title": article["title"],
            "summary": article["summary"],
            "category": article["category"],
            "url": article["url"],
            "sources": [article["source"]],
            "frequency": 1,
            "priority_keyword": True
        })

# Save highlights
with open(HIGHLIGHTS_JSON, "w", encoding="utf-8") as f:
    json.dump(highlight_data, f, indent=2)

print(f"📌 Highlights saved to {HIGHLIGHTS_JSON} ({len(highlight_data)} items)")
