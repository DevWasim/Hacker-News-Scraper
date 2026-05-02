
<p align="center">
  <b>🚀 A Hacker News scraper with an animated 3D galaxy visualization — zero external JS dependencies.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/vanilla_js-no_frameworks-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/zero_CDN-fully_local-00C853?style=for-the-badge" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" />
</p>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖥️ **CLI Mode** | Scrape and print top HN stories right in your terminal |
| 🌌 **3D Galaxy UI** | Animated starfield with orbiting story nodes — fully rendered on Canvas 2D |
| 🔗 **Local API** | Lightweight JSON API at `/api/stories` with filtering support |
| 🚫 **No CDN** | Works in restricted/offline networks — zero external JS dependencies |
| 🖱️ **Interactive** | Hover nodes for tooltips, click to open stories in a new tab |
| 📡 **Dual Sources** | Scrape HTML pages or use the reliable Algolia front-page API |

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/DevWasim/Hacker-News-Scraper.git
cd Hacker-News-Scraper

# Install Python dependencies
pip install requests beautifulsoup4
```

> **Requirements:** Python 3.8+ and a modern web browser.

---

## 🚀 Quick Start

### CLI Mode

Scrape top stories and print them in your terminal:

```bash
python hacker_news_scraper.py
```

### Web Mode (3D Galaxy)

Launch the local server and open the 3D visualization:

```bash
python hacker_news_scraper.py --serve
```

Then open **http://localhost:8000** in your browser.

You can also specify a custom port:

```bash
python hacker_news_scraper.py --serve --port 9000
```

---

## 🌐 API Reference

### `GET /api/stories`

Fetch filtered and sorted stories as JSON.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pages` | int | `2` | Number of pages to scrape (1–10) |
| `min_points` | int | `50` | Minimum score threshold |
| `source` | string | `front_page` | `front_page` (Algolia API) or `scrape` (HTML parsing) |

**Example Request:**

```bash
curl "http://localhost:8000/api/stories?pages=3&min_points=100&source=front_page"
```

**Example Response:**

```json
{
  "status": "success",
  "source": "front_page",
  "count": 18,
  "stories": [
    {
      "title": "Show HN: WhatCable",
      "link": "https://whatcable.app",
      "points": 430
    }
  ]
}
```

---

## 🧠 How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    hacker_news_scraper.py                │
│                                                         │
│   ┌─────────────┐    ┌──────────────┐                   │
│   │  CLI Mode    │    │  Web Server  │                   │
│   │  (Terminal)  │    │  (Port 8000) │                   │
│   └──────┬──────┘    └──────┬───────┘                   │
│          │                  │                            │
│          ▼                  ▼                            │
│   ┌─────────────────────────────────┐                   │
│   │         HNScraper Engine        │                   │
│   │  ┌───────────┐ ┌─────────────┐  │                   │
│   │  │  Scrape   │ │  Algolia    │  │                   │
│   │  │  (HTML)   │ │  (API)      │  │                   │
│   │  └───────────┘ └─────────────┘  │                   │
│   └──────────────┬──────────────────┘                   │
│                  │                                      │
│                  ▼                                      │
│   ┌─────────────────────────────────┐                   │
│   │   Filter → Sort → Serialize    │                   │
│   └─────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │     web_ui/index.html        │
        │  ┌────────┐  ┌───────────┐   │
        │  │ Story  │  │ 3D Galaxy │   │
        │  │ Cards  │  │ Canvas    │   │
        │  └────────┘  └───────────┘   │
        └──────────────────────────────┘
```

---

## 📁 Project Structure

```
Hacker-News-Scraper/
├── hacker_news_scraper.py    # Main script — CLI + API server
├── web_ui/
│   └── index.html            # Self-contained 3D galaxy frontend
└── README.md                 # You are here
```

---

## 🎨 3D Galaxy Visualization

The right panel renders a **real-time 3D story field** using pure Canvas 2D — no Three.js, no WebGL, no external libraries.

- **Node size** → Story points (higher score = bigger node)
- **Node glow** → Brightness scales with popularity
- **Orbital speed** → Higher-scoring stories orbit faster
- **Starfield** → 500+ twinkling stars with parallax drift
- **Nebula** → Radial gradient glow for depth atmosphere
- **Hover** → Tooltip shows story title and points
- **Click** → Opens the story link in a new tab

---

## ⚙️ Configuration

| CLI Argument | Description |
|---|---|
| `--serve` | Launch the web API server instead of CLI mode |
| `--port PORT` | Set server port (default: `8000`) |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---



```
  ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗     ███╗   ██╗███████╗██╗    ██╗███████╗
  ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗    ████╗  ██║██╔════╝██║    ██║██╔════╝
  ███████║███████║██║     █████╔╝ █████╗  ██████╔╝    ██╔██╗ ██║█████╗  ██║ █╗ ██║███████╗
  ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗    ██║╚██╗██║██╔══╝  ██║███╗██║╚════██║
  ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║    ██║ ╚████║███████╗╚███╔███╔╝███████║
  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝ ╚══════╝

███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
```


<p align="center">
  Built with 🧡 by <a href="https://github.com/DevWasim">DevWasim</a>
</p>
