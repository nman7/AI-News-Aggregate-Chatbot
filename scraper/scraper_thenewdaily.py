from scraper_base import get_soup, make_article

BASE_URL = "https://thenewdaily.com.au"

CATEGORY_URLS = {
    "sport": "https://thenewdaily.com.au/sport/",
    "lifestyle": "https://thenewdaily.com.au/life/",
    "music": "https://thenewdaily.com.au/entertainment/music/",
    "business": "https://thenewdaily.com.au/finance/"
}

def extract_newdaily_text(url):
    try:
        soup = get_soup(url)
        paragraphs = soup.select("p.text-article-body")  # More specific selector
        return " ".join(p.get_text(strip=True) for p in paragraphs).strip()
    except Exception as e:
        print(f"❌ Failed to extract full text from {url}: {e}")
        return ""

def fetch_newdaily_articles(category_name, url):
    articles = []
    soup = get_soup(url)
    seen_urls = set()

    for card in soup.select(".lg\\:grid-in-main .group"):
        try:
            a_tag = card.select_one("a[href]")
            title_tag = card.select_one("h1")
            if not a_tag or not title_tag:
                continue

            href = a_tag["href"]
            full_url = href if href.startswith("http") else BASE_URL + href
            if full_url in seen_urls:
                continue

            title = title_tag.get_text(strip=True)
            raw_text = extract_newdaily_text(full_url)

            article = make_article(
                title=title,
                url=full_url,
                source="The New Daily",
                category=category_name,
                summary="",
                raw_text=raw_text
            )
            articles.append(article)
            seen_urls.add(full_url)

        except Exception as e:
            print(f"⚠️ Error parsing article card: {e}")

    return articles
