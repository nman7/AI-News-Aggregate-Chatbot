import os
import json
from scraper_abc import fetch_abc_articles, CATEGORY_URLS as ABC_CATEGORY_URLS
from scraper_guardian import fetch_guardian_articles, CATEGORY_URLS as GUARDIAN_CATEGORY_URLS
from scraper_thenewdaily import fetch_newdaily_articles, CATEGORY_URLS as NEWDAILY_CATEGORY_URLS

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import RAW_JSON, NEWS_DATA_DIR

def run_all_scrapers():
    combined_data = {
        "ABC News": {},
        "The Guardian": {},
        "The New Daily": {}
    }

    for category, url in ABC_CATEGORY_URLS.items():
        print(f"🔎 Scraping ABC - {category}...")
        try:
            articles = fetch_abc_articles(category_name=category, url=url)
            combined_data["ABC News"][category] = articles
            print(f"✅ {len(articles)} articles added under ABC News → {category}")
        except Exception as e:
            print(f"❌ Failed ABC scrape for category {category}: {e}")

    for category, url in GUARDIAN_CATEGORY_URLS.items():
        print(f"🔎 Scraping Guardian - {category}...")
        try:
            articles = fetch_guardian_articles(category_name=category, url=url)
            combined_data["The Guardian"][category] = articles
            print(f"✅ {len(articles)} articles added under The Guardian → {category}")
        except Exception as e:
            print(f"❌ Failed Guardian scrape for category {category}: {e}")

    # for category, url in NEWDAILY_CATEGORY_URLS.items():
    #     print(f"🔎 Scraping New Daily - {category}...")
    #     try:
    #         articles = fetch_newdaily_articles(category_name=category, url=url)
    #         combined_data["The New Daily"][category] = articles
    #         print(f"✅ {len(articles)} articles added under The New Daily → {category}")
    #     except Exception as e:
    #         print(f"❌ Failed New Daily scrape for category {category}: {e}")

    os.makedirs(NEWS_DATA_DIR, exist_ok=True)
    with open(RAW_JSON, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2)

    print(f"🎉 All data saved to {RAW_JSON}")

if __name__ == "__main__":
    run_all_scrapers()
