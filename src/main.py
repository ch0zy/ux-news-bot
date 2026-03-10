import logging
import yaml
from datetime import date
from pathlib import Path

from news_fetcher import fetch_news
from thumbnail_extractor import extract_thumbnails
from summarizer import summarize_articles, generate_one_liner
from email_builder import build_email
from sender import send_email

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def load_config() -> dict:
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    logger.info("Fetching news...")
    articles = fetch_news(config)
    logger.info("Found %d articles", len(articles))

    logger.info("Extracting thumbnails...")
    articles = extract_thumbnails(articles)

    logger.info("Summarizing articles...")
    articles = summarize_articles(articles, config)
    one_liner = generate_one_liner(articles)
    logger.info("One-liner: %s", one_liner)

    week_date = date.today().strftime("%B %d, %Y")
    subject = f"UX Weekly Digest — Week of {week_date}"

    logger.info("Building email...")
    html = build_email(one_liner, articles, week_date)

    logger.info("Sending email...")
    send_email(html, subject)
    logger.info("Done.")


if __name__ == "__main__":
    main()
