from scraper_base import get_soup, make_article

BASE_URL = "https://www.abc.net.au"

CATEGORY_URLS = {
    "sport": "https://www.abc.net.au/news/sport/",
    "lifestyle": "https://www.abc.net.au/news/lifestyle/",
    "music": "https://www.abc.net.au/news/topic/music",
    "business": "https://www.abc.net.au/news/business/"
}

def extract_summary_and_raw_text(url):
    try:
        soup = get_soup(url)

        # --- Extract "In Short" Summary ---
        summary = ""
        summary_block = soup.select_one("div.Article_main___guM5")
        if summary_block:
            lines = []
            found = False
            for el in summary_block.find_all(recursive=False):
                if el.name == "h2" and "in short" in el.get_text(strip=True).lower():
                    found = True
                    continue
                if found:
                    if el.name == "h2":
                        break
                    if el.name == "p":
                        lines.append(el.get_text(strip=True))
            summary = " ".join(lines).strip()

        # --- Extract Full Raw Text ---
        raw_text = ""
        article_body = soup.select_one("div.ArticleRender_article__7i2EW")
        if article_body:
            paragraphs = [p.get_text(strip=True) for p in article_body.find_all("p")]
            raw_text = " ".join(paragraphs).strip()

        return summary, raw_text

    except Exception as e:
        print(f"❌ Failed to extract: {url} → {e}")
        return "", ""

def fetch_abc_articles(category_name, url):
    articles = []
    soup = get_soup(url)

    # Try to locate the correct <ul> for this category
    ul_block = None
    for ul in soup.select("ul.FeaturedCollection_layout__kEyQk"):
        if category_name.lower() in ul.get_text(strip=True).lower():
            ul_block = ul
            break

    if not ul_block:
        ul_block = soup.select_one("ul.FeaturedCollection_layout__kEyQk")

    if not ul_block:
        print(f"❌ No article list found for: {category_name}")
        return []

    for card in ul_block.select("li.FeaturedCollection_cardList__lnpB_"):
        try:
            a_tag = card.select_one("h3 a")
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            href = a_tag.get("href", "")
            full_url = href if href.startswith("http") else BASE_URL + href

            summary, raw_text = extract_summary_and_raw_text(full_url)

            article = make_article(
                title=title,
                url=full_url,
                source="ABC News",
                category=category_name,
                summary=summary,
                raw_text=raw_text
            )
            articles.append(article)

        except Exception as e:
            print(f"⚠️ Failed to parse card: {e}")

    return articles
