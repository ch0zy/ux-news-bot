# UX Weekly Digest Bot

Automated weekly email digest of UX design, AI tools, and government digital services news. Runs every Friday at 9:00am UTC+8 via GitHub Actions.

## Stack

| Component | Tool |
|-----------|------|
| Scheduler | GitHub Actions (cron) |
| News search | Tavily API |
| Summarization | Claude Haiku (`claude-haiku-4-5-20251001`) |
| Email delivery | Gmail SMTP |
| Template | Jinja2 (responsive HTML) |

## Setup

### 1. Fork / clone this repo

### 2. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|--------|-------------|
| `TAVILY_API_KEY` | Free tier at [tavily.com](https://tavily.com) |
| `ANTHROPIC_API_KEY` | From [console.anthropic.com](https://console.anthropic.com) |
| `GMAIL_ADDRESS` | Sender Gmail address |
| `GMAIL_APP_PASSWORD` | Gmail App Password (see below) |
| `RECIPIENT_EMAILS` | Comma-separated: `alice@co.com,bob@co.com` |

### 3. Gmail App Password

1. Enable 2FA on the sender Gmail account
2. Go to Google Account → Security → App Passwords
3. Create a password for "Mail" / "Other"
4. Store the 16-character result as `GMAIL_APP_PASSWORD`

### 4. Customize search topics

Edit `config.yaml` to change search queries, number of articles, or summary length.

## Local Testing

```bash
pip install -r requirements.txt

# Set env vars (or use a .env file with `export $(cat .env | xargs)`)
export TAVILY_API_KEY=...
export ANTHROPIC_API_KEY=...
export GMAIL_ADDRESS=...
export GMAIL_APP_PASSWORD=...
export RECIPIENT_EMAILS=you@example.com

python src/main.py
```

### Preview email template

```bash
python src/email_builder.py
open preview.html
```

## Manual Trigger

In the GitHub UI: **Actions → Weekly UX News Digest → Run workflow**

## Updating Recipients

Edit the `RECIPIENT_EMAILS` secret in GitHub Settings. No code changes needed.
