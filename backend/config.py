# === config.py === (shared between backend and scraper)
import os

ENV = os.getenv("ENV", "development")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRAPER_DIR = os.path.join(BASE_DIR, "scraper")
NEWS_DATA_DIR = os.path.join(SCRAPER_DIR, "news_data")

RAG_INDEX_DIR = os.path.join(SCRAPER_DIR, "rag_index")

RAW_JSON = os.path.join(NEWS_DATA_DIR, "combined_articles.json")
SUMMARY_JSON = os.path.join(NEWS_DATA_DIR, "combined_articles_with_summary.json")
HIGHLIGHTS_JSON = os.path.join(NEWS_DATA_DIR, "combined_articles_with_summary_highlights.json")

MODEL_NAME = os.getenv("MODEL_NAME", "t5-small")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
GEN_MODEL_NAME = "declare-lab/flan-alpaca-base"

# FAISS
FAISS_INDEX_FILE = os.path.join(RAG_INDEX_DIR, "highlight_index.faiss")
METADATA_FILE = os.path.join(RAG_INDEX_DIR, "metadata.json")

# Thresholds
COSINE_THRESHOLD = float(os.getenv("COSINE_THRESHOLD", 0.5))
MAX_SUMMARY_WORDS = int(os.getenv("MAX_SUMMARY_WORDS", 60))
MAX_CHARS = int(os.getenv("MAX_CHARS", 500))

