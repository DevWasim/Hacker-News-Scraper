"""Hacker News scraper + local API server."""
"""Hacker News scraper + tiny API server.

Usage:
  python hacker_news_scraper.py              # interactive CLI mode
  python hacker_news_scraper.py --serve      # start web API for the 3D UI
"""
from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import List
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup

# --- Global Config ---
BASE_URL = "https://news.ycombinator.com/news?p={page}"
ALGOLIA_URL = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage={limit}"
DEFAULT_MIN_POINTS = 50

# Setup logging with some personality
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

@dataclass(frozen=True)
class Story:
    """Immutable data container for an HN Story."""
    title: str
    link: str
    points: int

class HNScraper:
    """The engine room. Responsible for pulling data from the orange site."""
    
    @staticmethod
    def fetch_via_scraping(page: int) -> List[Story]:
        """
        Dives into the HTML soup to extract stories.
        Handles the mismatch between title rows and metadata rows gracefully.
        """
        stories = []
        try:
            response = requests.get(BASE_URL.format(page=page), timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # HN structure: '.athing' contains the title, the next 'tr' contains the score
            rows = soup.select(".athing")
            for row in rows:
                subtext = row.find_next_sibling("tr")
                if not subtext: 
                    continue
                
                score_element = subtext.select_one(".score")
                # Skip job postings or ads that don't have upvotes
                if not score_element: 
                    continue
                
                points = int(score_element.get_text(strip=True).split()[0])
                link_element = row.select_one(".titleline > a")
                
                if link_element:
                    stories.append(Story(
                        title=link_element.get_text(strip=True),
                        link=link_element.get("href", ""),
                        points=points
                    ))
        except Exception as e:
            logging.error(f"Scraping heist failed on page {page}: {e}")
        return stories

    @staticmethod
    def fetch_via_api(limit: int = 100) -> List[Story]:
        """
        Fallback mechanism using the Algolia API. 
        Because sometimes HTML tags change, but APIs (mostly) don't.
        """
        try:
            response = requests.get(ALGOLIA_URL.format(limit=limit), timeout=10)
            response.raise_for_status()
            hits = response.json().get("hits", [])
            return [
                Story(
                    title=h.get("title") or "Untitled Story",
                    link=h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                    points=h.get("points", 0)
                ) for h in hits
            ]
        except Exception as e:
            logging.error(f"API fallback went sideways: {e}")
            return []

def get_curated_stories(num_pages: int, min_points: int, use_api: bool = False) -> List[Story]:
    """
    The brain of the operation: Fetches, filters out the noise, and sorts by hype (points).
    """
    raw_data = []
    
    if use_api:
        logging.info(f"Fetching {num_pages * 30} stories via Algolia API...")
        raw_data = HNScraper.fetch_via_api(limit=num_pages * 30)
    else:
        logging.info(f"Scraping {num_pages} page(s) from Hacker News...")
        for p in range(1, num_pages + 1):
            raw_data.extend(HNScraper.fetch_via_scraping(p))
    
    # Filter by user-defined quality threshold (min_points)
    refined = [s for s in raw_data if s.points >= min_points]
    return sorted(refined, key=lambda x: x.points, reverse=True)

class HNRequestHandler(BaseHTTPRequestHandler):
    """
    A lightweight handler to serve the UI and API endpoints.
    Built with zero external dependencies (Vanilla Python).
    """
    
    static_root = Path(__file__).resolve().parent / "web_ui"

    def _respond_json(self, data: dict, status: int = 200):
        """Helper to ship JSON payloads with CORS enabled."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  # Modern UI needs CORS
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        
        # Endpoint: /api/stories?pages=2&min_points=100&source=scrape
        if url.path == "/api/stories":
            query = parse_qs(url.query)
            try:
                pages = int(query.get("pages", [2])[0])
                min_pts = int(query.get("min_points", [DEFAULT_MIN_POINTS])[0])
                source = query.get("source", ["scrape"])[0]
                
                results = get_curated_stories(pages, min_pts, use_api=(source == "front_page"))
                self._respond_json({
                    "status": "success",
                    "source": source,
                    "stories": [asdict(s) for s in results],
                    "count": len(results)
                })
            except Exception as e:
                self._respond_json({"error": str(e)}, 400)
            return

        # Serve static frontend (index.html)
        if url.path in {"/", "/index.html"}:
            index_path = self.static_root / "index.html"
            if index_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(index_path.read_bytes())
            else:
                self.send_error(404, "Frontend UI not found in /web_ui")
            return

        self.send_error(404)

def main():
    """Entry point for CLI and Server modes."""
    parser = argparse.ArgumentParser(description="Hacker News Master Scraper")
    parser.add_argument("--serve", action="store_true", help="Launch the local API server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()

    if args.serve:
        server = ThreadingHTTPServer(("0.0.0.0", args.port), HNRequestHandler)
        logging.info(f"🚀 API ready at http://localhost:{args.port}/api/stories")
        logging.info(f"🌐 UI ready at http://localhost:{args.port}")
        server.serve_forever()
    else:
        # CLI Mode: Quick and dirty
        try:
            print("\n--- HN CLI Explorer ---")
            pages = int(input("How many pages to scan? (default 1): ") or 1)
            stories = get_curated_stories(pages, DEFAULT_MIN_POINTS)
            
            for i, s in enumerate(stories, 1):
                print(f"{i:02d}. [{s.points:4} pts] {s.title}")
                print(f"    🔗 {s.link}\n")
        except KeyboardInterrupt:
            print("\nAborted by user. Happy hacking!")

if __name__ == "__main__":
    main()
