# Hacker News Scraper + Animated 3D UI

A reliable Hacker News scraper with:

- **CLI mode** (scrape and print top stories)
- **Web mode** with a **local 3D animated galaxy UI**
- **No external front-end CDN dependency** (works in restricted networks)
# Hacker News Scraper + 3D Three.js UI

A Hacker News scraper that now has:

- **CLI mode** (scrape and print top stories in your terminal)
- **Web mode** with a **Three.js galaxy interface** where stories become animated 3D nodes

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


Tip: Use `source=front_page` for the most stable results.
You will be prompted for number of pages to scrape.

## Run the 3D web experience

```bash
python hacker_news_scraper.py --serve
```

Then open:

- <http://127.0.0.1:8000>

### Web features

- Animated starfield and orbiting story nodes via Three.js
- Adjustable pages and minimum score filters
- Story cards synced with 3D visualization
- Lightweight local JSON API at `/api/stories`

## API

`GET /api/stories?pages=2&min_points=50`

Response shape:

```json
{
  "stories": [
    {
      "title": "Example",
      "link": "https://example.com",
      "points": 123
    }
  ]
}
```
