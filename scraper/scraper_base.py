import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}



def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")

def make_article(title, url, source, category, summary=None, raw_text=None):
    return {
        "title": title.strip(),
        "url": url,
        "source": source,
        "category": category,
        "summary": summary or "",
        "raw_text": raw_text or "",
        "scraped_at": datetime.now().isoformat()
    }
