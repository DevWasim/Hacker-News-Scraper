# Hacker News Scraper + Animated 3D UI

A reliable Hacker News scraper with:

- **CLI mode** (scrape and print top stories)
- **Web mode** with a **local 3D animated galaxy UI**
- **No external front-end CDN dependency** (works in restricted networks)

## Setup

```bash
pip install requests beautifulsoup4
```

## Run in CLI mode

```bash
python hacker_news_scraper.py
```

## Run the web app

```bash
python hacker_news_scraper.py --serve
```

Open:

- <http://127.0.0.1:8000>

## Why this version is more reliable

- UI animation is fully local (no module imports from blocked CDNs)
- `/api/stories` supports `source=front_page` (default, most reliable) and `source=scrape`
- Better error messages in the UI

## API

`GET /api/stories?pages=2&min_points=50&source=front_page`

Optional:

- `source=front_page` to use Algolia front-page source directly
