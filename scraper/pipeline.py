import subprocess

steps = [
    ("🕸️ Scraping all news sources", "python scraper/scraper_manager.py"),
    ("🧠 Generating summaries", "python scraper/create_summary.py"),
    ("📌 Creating news highlights", "python scraper/create_highlights.py"),
    ("📂 Building FAISS index", "python scraper/create_faiss_index.py"),
]

for desc, cmd in steps:
    print("\n" + "=" * 60)
    print(f"{desc}...\nRunning: {cmd}")
    print("=" * 60)
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Completed: {desc}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed during step: {desc}")
        print(f"Error: {e}")
        break
else:
    print("\n🎉 ALL DONE — Pipeline completed successfully!")
