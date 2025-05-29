import os
import json
from scraper_abc import fetch_abc_articles, CATEGORY_URLS as ABC_CATEGORY_URLS
from scraper_guardian import fetch_guardian_articles, CATEGORY_URLS as GUARDIAN_CATEGORY_URLS

def run_all_scrapers():
    combined_data = {
        "ABC News": {},
        "The Guardian": {}
    }



    # Scrape ABC News
    for category, url in ABC_CATEGORY_URLS.items():
        print(f"🔎 Scraping ABC - {category}...")
        try:
            articles = fetch_abc_articles(category_name=category, url=url)
            combined_data["ABC News"][category] = articles
            print(f"✅ {len(articles)} articles added under ABC News → {category}")
        except Exception as e:
            print(f"❌ Failed ABC scrape for category {category}: {e}")

    # Save to file
    os.makedirs("data", exist_ok=True)
    with open("data/combined_articles.json", "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2)

    print("🎉 All data saved to data/combined_articles.json")

if __name__ == "__main__":
    run_all_scrapers()
