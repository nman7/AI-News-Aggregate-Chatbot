# run_pipeline.py
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

steps = [
    ("Scraping news", "python3 scraper/scraper_manager.py"),
    ("Generating summaries", "python3 scraper/create_summary.py"),
    ("Creating highlights", "python3 scraper/create_highlights.py"),
    ("Building FAISS index", "python3 scraper/create_faiss_index.py"),
]

for desc, cmd in steps:
    logging.info(f"Running: {desc}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        logging.info(f"✅ {desc} complete")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Failed at step: {desc} | Error: {e}")
        break