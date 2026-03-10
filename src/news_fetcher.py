import os
from tavily import TavilyClient


def fetch_news(config: dict) -> list[dict]:
    """Query Tavily for each search query, deduplicate by URL, return top N articles."""
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    queries = config["search_queries"]
    results_per_query = config.get("results_per_query", 5)
    max_articles = config.get("max_articles", 10)

    seen_urls = set()
    articles = []

    for query in queries:
        response = client.search(
            query=query,
            search_depth="advanced",
            include_answer=False,
            max_results=results_per_query,
        )
        for result in response.get("results", []):
            url = result.get("url")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            articles.append({
                "title": result.get("title", ""),
                "url": url,
                "content": result.get("content", ""),
                "published_date": result.get("published_date", ""),
            })

    # Sort by published_date descending (empty strings sort to end)
    articles.sort(key=lambda a: a["published_date"] or "", reverse=True)

    return articles[:max_articles]
