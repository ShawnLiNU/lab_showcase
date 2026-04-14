#!/usr/bin/env python3
"""
Lab Showcase Server
===================
A simple local server that serves the showcase webpage and
automatically discovers photos, videos, and descriptions.

USAGE:
    python3 server.py
    Then open http://localhost:8080 in a full-screen browser.

OPTIONS:
    python3 server.py -title "My Lab"   # Display name (top-left corner)
    python3 server.py -time 10          # Seconds per slide (default: 8)
    python3 server.py -port 9090        # Use a different port

EXAMPLES:
    python3 server.py -title "ECE Robotics Lab" -time 12
    python3 server.py -title "EECE 5552 · Assistive Robotics" -time 6 -port 8888
"""

import http.server
import json
import os
import sys
import argparse
from pathlib import Path
from urllib.parse import unquote

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.resolve()
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".ogg"}

# ---------------------------------------------------------------------------
# Content scanner
# ---------------------------------------------------------------------------
def scan_content():
    """Walk /photos and /videos, pair each with a .txt from /words."""
    slides = []

    # Scan photos
    photos_dir = BASE_DIR / "photos"
    if photos_dir.is_dir():
        for f in sorted(photos_dir.iterdir()):
            if f.suffix.lower() in PHOTO_EXTENSIONS:
                slides.append(_build_slide(f, "photo"))

    # Scan videos
    videos_dir = BASE_DIR / "videos"
    if videos_dir.is_dir():
        for f in sorted(videos_dir.iterdir()):
            if f.suffix.lower() in VIDEO_EXTENSIONS:
                slides.append(_build_slide(f, "video"))

    return slides


def _build_slide(filepath, media_type):
    """Build a slide dict for one media file."""
    stem = filepath.stem                         # e.g. "exoskeleton"
    title = stem.replace("-", " ").replace("_", " ").title()

    # Look for matching .txt in /words
    txt_path = BASE_DIR / "words" / (stem + ".txt")
    description = ""
    if txt_path.is_file():
        description = txt_path.read_text(encoding="utf-8").strip()

    # Relative URL path from the showcase root
    rel = filepath.relative_to(BASE_DIR).as_posix()

    return {
        "type": media_type,
        "src": rel,
        "title": title,
        "description": description,
    }


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------
class ShowcaseHandler(http.server.SimpleHTTPRequestHandler):
    """Extends the default file server with an /api/slides endpoint."""

    def __init__(self, *args, interval=8, title="Lab Showcase", **kwargs):
        self.interval = interval
        self.title = title
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        path = unquote(self.path).split("?")[0]

        if path == "/api/slides":
            slides = scan_content()
            payload = json.dumps({
                "slides": slides,
                "interval": self.interval,
                "title": self.title,
            }, ensure_ascii=False)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(payload.encode("utf-8"))
            return

        # Everything else: serve static files normally
        super().do_GET()

    def log_message(self, format, *args):
        # Quieter logging — only show non-200 or API hits
        if "/api/" in str(args[0]) or "200" not in str(args[1]):
            super().log_message(format, *args)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Lab Showcase Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-title", type=str, default="Lab Showcase",
                        help='Display name shown top-left (default: "Lab Showcase")')
    parser.add_argument("-time", type=int, default=8,
                        help="Seconds per slide (default: 8)")
    parser.add_argument("-port", type=int, default=8080,
                        help="Server port (default: 8080)")
    args = parser.parse_args()

    # Inject settings into handler via a factory
    def handler_factory(*h_args, **h_kwargs):
        return ShowcaseHandler(*h_args, interval=args.time, title=args.title, **h_kwargs)

    server = http.server.HTTPServer(("0.0.0.0", args.port), handler_factory)
    print(f"""
╔══════════════════════════════════════════════════════════╗
║             🤖  LAB SHOWCASE SERVER  🤖                 ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Title:            {args.title:<37} ║
║  Open in browser:  http://localhost:{args.port:<21} ║
║  Slide interval:   {args.time} seconds{' ' * max(0, 30 - len(str(args.time)))}║
║                                                          ║
║  Folder structure:                                       ║
║    /photos/   ← Drop .jpg .png .webp images here         ║
║    /videos/   ← Drop .mp4 .webm clips here               ║
║    /words/    ← Drop .txt descriptions here               ║
║                                                          ║
║  Press Ctrl+C to stop.                                   ║
╚══════════════════════════════════════════════════════════╝
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
