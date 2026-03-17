import os
import anthropic

MODEL = "claude-haiku-4-5-20251001"


def summarize_articles(articles: list[dict], config: dict) -> list[dict]:
    """Add a short summary to each article using Claude."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    max_words = config.get("summary_max_words", 20)

    for article in articles:
        prompt = (
            f"Summarize this article in {max_words} words or fewer. "
            f"Return only the summary, no preamble.\n\n"
            f"Title: {article['title']}\n"
            f"Snippet: {article['content']}"
        )
        response = client.messages.create(
            model=MODEL,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )
        article["summary"] = response.content[0].text.strip()

    return articles


def generate_one_liner(articles: list[dict]) -> str:
    """Generate a weekly one-liner summarizing all articles."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    titles = ", ".join(a["title"] for a in articles)

    prompt = (
        "Write one engaging sentence (max 25 words) summarizing this week's top stories "
        "in UX design, AI tools, and government digital services. "
        "Return only the sentence — no markdown, no headers, no preamble.\n\n"
        f"Topics: {titles}"
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=80,
        messages=[{"role": "user", "content": prompt}],
    )
    # Strip any leading markdown heading markers the model occasionally emits
    text = response.content[0].text.strip()
    return text.lstrip('#').strip()
