import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


def _fetch_og_image(url: str) -> str | None:
    try:
        resp = requests.get(url, timeout=3, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        tag = soup.find("meta", property="og:image")
        if tag and tag.get("content"):
            return tag["content"]
    except Exception:
        pass
    return None


def extract_thumbnails(articles: list[dict]) -> list[dict]:
    """Fetch og:image for each article concurrently, attach as thumbnail_url."""
    urls = [a["url"] for a in articles]

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_index = {executor.submit(_fetch_og_image, url): i for i, url in enumerate(urls)}
        results = [None] * len(urls)
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            results[idx] = future.result()

    for article, thumbnail in zip(articles, results):
        article["thumbnail_url"] = thumbnail

    return articles
