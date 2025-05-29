from scraper_base import make_article, get_soup

CATEGORY_URLS = {
    "sport": "https://www.theguardian.com/au/sport",
    "business": "https://www.theguardian.com/au/business",
    "music": "https://www.theguardian.com/music",
    "lifestyle": "https://www.theguardian.com/au/lifeandstyle"
}

CONTAINER_IDS = {
    "sport": "container-sport",
    "business": "container-news",
    "music": "container-music",
    "lifestyle": "container-lifestyle"
}

def extract_guardian_article(url):
    try:
        soup = get_soup(url)
        paragraphs = soup.select("div[data-gu-name='body'] p")
        return " ".join(p.get_text(strip=True) for p in paragraphs)
    except Exception as e:
        print(f"❌ Failed to extract full text from {url}: {e}")
        return ""

def fetch_guardian_articles(category_name, url):
    articles = []
    seen_urls = set()  # ✅ Set to track already seen article URLs

    try:
        soup = get_soup(url)
        container_id = CONTAINER_IDS.get(category_name)
        container = soup.find("div", id=container_id)

        if not container:
            print(f"❌ No container found for {category_name}")
            return []

        li_elements = container.select("ul li")
        for li in li_elements:
            a_tag = li.find("a", href=True)
            if not a_tag:
                continue

            href = a_tag["href"]
            full_url = href if href.startswith("http") else f"https://www.theguardian.com{href}"

            if full_url in seen_urls:  # ✅ Skip duplicates
                continue
            seen_urls.add(full_url)

            title = a_tag.get("aria-label") or a_tag.get_text(strip=True)
            full_text = extract_guardian_article(full_url)

            article = make_article(
                title=title,
                url=full_url,
                source="The Guardian Australia",
                category=category_name,
                summary="",
                raw_text=full_text
            )
            articles.append(article)

    except Exception as e:
        print(f"❌ Error scraping {category_name}: {e}")

    print(f"✅ {len(articles)} articles scraped for {category_name}")
    return articles
