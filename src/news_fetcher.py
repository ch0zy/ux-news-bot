import logging
import os

from tavily import TavilyClient

logger = logging.getLogger(__name__)


def fetch_news(config: dict) -> list[dict]:
    """Query Tavily for each search query, deduplicate by URL, return top N articles.

    Each query is constrained to the past 7 days via Tavily's `days` parameter so
    that only this week's news is returned. A warning is logged whenever a query
    produces fewer results than `min_results_per_query` (default 2).
    """
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    queries = config["search_queries"]
    results_per_query = config.get("results_per_query", 7)
    min_results_per_query = config.get("min_results_per_query", 2)
    max_articles = config.get("max_articles", 10)

    seen_urls: set[str] = set()
    articles: list[dict] = []

    for query in queries:
        response = client.search(
            query=query,
            search_depth="advanced",
            topic="news",        # constrain to news articles
            days=7,              # only return articles from the past 7 days
            include_answer=False,
            max_results=results_per_query,
        )
        results = response.get("results", [])

        new_for_query: list[dict] = []
        for result in results:
            url = result.get("url")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            article = {
                "title": result.get("title", ""),
                "url": url,
                "content": result.get("content", ""),
                "published_date": result.get("published_date", ""),
            }
            articles.append(article)
            new_for_query.append(article)

        if len(new_for_query) < min_results_per_query:
            logger.warning(
                "Query returned only %d new article(s) (min %d expected): %r",
                len(new_for_query),
                min_results_per_query,
                query,
            )
        else:
            logger.info("Query yielded %d new article(s): %r", len(new_for_query), query)

    # Sort by published_date descending (empty strings sort to end)
    articles.sort(key=lambda a: a["published_date"] or "", reverse=True)

    return articles[:max_articles]
