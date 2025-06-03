import os
import json
from collections import Counter
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the local model
# model = SentenceTransformer("scraper/highlights_model/all-MiniLM-L6-v2")
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load articles
with open("scraper/news_data/combined_articles_with_summary.json", "r", encoding="utf-8") as f:
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
                # "raw_text": raw_text
            })

print(f"✅ Total articles loaded: {len(all_articles)}")

# Generate embeddings from title + summary
texts = [a["title"] + " " + a["summary"] for a in all_articles]
embeddings = model.encode(texts, batch_size=16, show_progress_bar=True)

# Compute cosine similarity matrix
sim_matrix = cosine_similarity(embeddings)

# Cluster similar articles
THRESHOLD = 0.60
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

# === PRIORITIZE keyword-based highlights ===
import re

priority_keywords = [
    "breaking",
    "exclusive",
    "alert",
    "just in",
    "urgent",
    "live",
    "update",
    "developing",
    "confirmed",
    "shocking"
]

def is_priority_article(article):
    title = article.get("title", "").lower()
    for kw in priority_keywords:
        if re.search(rf"\b{re.escape(kw)}\b", title):
            print(f"✅ Matched keyword: '{kw}' in title: '{title}'")
            return True
    return False

# Cluster-based highlights
highlight_data = []
for cluster in clusters:
    sources = [all_articles[i]["source"] for i in cluster]
    main_idx = cluster[0]
    highlight_data.append({
        "title": all_articles[main_idx]["title"],
        "summary": all_articles[main_idx]["summary"],
        "category": all_articles[main_idx]["category"],
        "url": all_articles[main_idx]["url"],
        # "raw_text": all_articles[main_idx]["raw_text"],
        "sources": list(set(sources)),
        "frequency": len(cluster)
    })

# Keyword-priority highlights (if not already in clustered ones)
used_urls = {item["url"] for item in highlight_data}
for article in all_articles:
    if article["url"] not in used_urls and is_priority_article(article):
        print("--------------", article["title"])
        highlight_data.append({
            "title": article["title"],
            "summary": article["summary"],
            "category": article["category"],
            "url": article["url"],
            # "raw_text": article["raw_text"],
            "sources": [article["source"]],
            "frequency": 1,
            "priority_keyword": True
        })

# Save highlights
with open("scraper/news_data/combined_articles_with_summary_highlights.json", "w", encoding="utf-8") as f:
    json.dump(highlight_data, f, indent=2)

print(f"📌 Highlights saved to scraper/news_data/combined_articles_with_summary_highlights.json ({len(highlight_data)} items)")
