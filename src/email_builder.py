import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def build_email(one_liner: str, articles: list[dict], week_date: str) -> str:
    """Render the HTML email from the Jinja2 template."""
    templates_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template("digest.html.j2")

    return template.render(
        one_liner=one_liner,
        articles=articles,
        week_date=week_date,
    )


if __name__ == "__main__":
    # Standalone preview: output preview.html
    sample_articles = [
        {
            "title": "How AI is reshaping government UX",
            "url": "https://example.com/article1",
            "summary": "AI tools are transforming how governments design citizen-facing services.",
            "thumbnail_url": None,
            "published_date": "2026-03-07",
        },
        {
            "title": "Top UX research tools of 2026",
            "url": "https://example.com/article2",
            "summary": "New tools are making usability testing faster and more accessible.",
            "thumbnail_url": "https://placehold.co/600x150",
            "published_date": "2026-03-06",
        },
    ]
    html = build_email(
        one_liner="This week: AI, government UX, and the future of design research.",
        articles=sample_articles,
        week_date="March 10, 2026",
    )
    out = Path(__file__).parent.parent / "preview.html"
    out.write_text(html)
    print(f"Preview written to {out}")
