import os
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# === CONFIGURATION ===
MODEL_DIR = "./local_models/distilbart-cnn-12-6"
INPUT_JSON = "data/combined_articles.json"
OUTPUT_JSON = "data/combined_articles_with_summary.json"
MAX_CHARS = 1000  # truncate long raw_text for speed
MAX_SUMMARY_WORDS = 60

# === LOAD LOCAL MODEL ===
print("🧠 Loading model from local directory...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# === LOAD JSON DATA ===
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

updated_count = 0

# === GENERATE SUMMARIES ===
for source, categories in data.items():
    for category, articles in categories.items():
        for article in articles:
            if not article.get("summary") and article.get("raw_text"):
                try:
                    raw_text = article["raw_text"].replace("\n", " ").strip()
                    if len(raw_text) < 50:
                        continue  # skip very short text

                    text = raw_text[:MAX_CHARS]
                    result = summarizer(text, max_length=MAX_SUMMARY_WORDS, min_length=20, do_sample=False)
                    article["summary"] = result[0]["summary_text"]
                    updated_count += 1
                except Exception as e:
                    print(f"❌ Error summarizing: {article.get('url', 'unknown')} → {e}")

# === SAVE UPDATED JSON ===
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"✅ {updated_count} summaries added → saved to {OUTPUT_JSON}")
