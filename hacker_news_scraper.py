"""Hacker News scraper + tiny API server.

Usage:
  python hacker_news_scraper.py              # interactive CLI mode
  python hacker_news_scraper.py --serve      # start web API for the 3D UI
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import List
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://news.ycombinator.com/news?p={page}"
DEFAULT_MIN_POINTS = 50


@dataclass
class Story:
    title: str
    link: str
    points: int


def fetch_page(page: int, timeout: int = 15) -> tuple[list, list]:
    """Fetch one Hacker News page and return title + score elements."""
    response = requests.get(BASE_URL.format(page=page), timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.select(".titleline")
    votes = soup.select(".score")
    return links, votes


def parse_stories(links: list, votes: list, min_points: int = DEFAULT_MIN_POINTS) -> List[Story]:
    """Convert page elements to Story models filtered by points."""
    stories: List[Story] = []
    for link, vote in zip(links, votes):
        link_element = link.select_one("a")
        if not link_element:
            continue

        raw_score = vote.get_text(strip=True).replace(" points", "").replace(" point", "")
        points = int(raw_score)
        if points < min_points:
            continue

        stories.append(
            Story(
                title=link_element.get_text(strip=True),
                link=link_element.get("href", ""),
                points=points,
            )
        )
    return stories


def scrape_hn_pages(num_pages: int, min_points: int = DEFAULT_MIN_POINTS) -> List[Story]:
    """Scrape and return top stories from N pages, sorted by points."""
    if num_pages <= 0:
        return []

    all_stories: List[Story] = []
    for page in range(1, num_pages + 1):
        links, votes = fetch_page(page)
        all_stories.extend(parse_stories(links, votes, min_points=min_points))

    return sorted(all_stories, key=lambda item: item.points, reverse=True)


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class HNRequestHandler(BaseHTTPRequestHandler):
    """Serves static UI and a JSON endpoint."""

    static_root = Path(__file__).resolve().parent / "web_ui"

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)

        if parsed.path == "/api/stories":
            query = parse_qs(parsed.query)
            pages = int(query.get("pages", ["2"])[0])
            min_points = int(query.get("min_points", [str(DEFAULT_MIN_POINTS)])[0])
            try:
                stories = [asdict(story) for story in scrape_hn_pages(pages, min_points=min_points)]
            except Exception as exc:  # pragma: no cover - defensive for server mode
                _json_response(self, 500, {"error": str(exc)})
                return

            _json_response(self, 200, {"stories": stories})
            return

        if parsed.path in {"/", "/index.html"}:
            index_file = self.static_root / "index.html"
            body = index_file.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):  # noqa: A003
        return


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), HNRequestHandler)
    print(f"Serving 3D HN UI at http://{host}:{port}")
    server.serve_forever()


def run_cli() -> None:
    pages = int(input("How many pages do you want to scan? ").strip() or "1")
    stories = scrape_hn_pages(pages)
    for index, story in enumerate(stories, start=1):
        print(f"{index:>2}. [{story.points:>4} pts] {story.title}\n    {story.link}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Hacker News scraper")
    parser.add_argument("--serve", action="store_true", help="Run the local API + 3D web UI")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    args = parser.parse_args()

    if args.serve:
        run_server(host=args.host, port=args.port)
    else:
        run_cli()


if __name__ == "__main__":
    main()
