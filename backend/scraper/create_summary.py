import os
import json
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Setup config import
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import MODEL_NAME, RAW_JSON, SUMMARY_JSON, MAX_CHARS, MAX_SUMMARY_WORDS

BATCH_SIZE = 8  # local-only config

# === START TIMER ===
start_time = time.time()

# === LOAD MODEL ===
print("🧠 Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device=-1)

# === LOAD JSON DATA ===
with open(RAW_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

updated_count = 0
batch_number = 1

# === GENERATE SUMMARIES IN BATCHES ===
for source, categories in data.items():
    for category, articles in categories.items():
        texts_to_summarize = []
        article_refs = []

        for article in articles:
            if not article.get("summary") and article.get("raw_text"):
                raw_text = article["raw_text"].replace("\n", " ").strip()
                if len(raw_text) < 50:
                    continue
                text = raw_text[:MAX_CHARS]
                texts_to_summarize.append(text)
                article_refs.append(article)

        for i in range(0, len(texts_to_summarize), BATCH_SIZE):
            batch = texts_to_summarize[i:i + BATCH_SIZE]
            try:
                results = summarizer(batch, max_length=MAX_SUMMARY_WORDS, min_length=20, do_sample=False)
                for j, result in enumerate(results):
                    article_refs[i + j]["summary"] = result["summary_text"]
                    updated_count += 1
                print(f"✅ Completed Batch #{batch_number}")
                batch_number += 1
            except Exception as e:
                print(f"❌ Error summarizing batch starting at index {i}: {e}")

# === SAVE UPDATED JSON ===
with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

elapsed_time = time.time() - start_time
print(f"✅ {updated_count} summaries added → saved to {SUMMARY_JSON}")
print(f"⏱️ Total processing time: {elapsed_time:.2f} seconds")
