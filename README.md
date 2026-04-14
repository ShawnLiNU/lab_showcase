# Lab Showcase

A file-driven slideshow for lab big screens. Drop photos and videos into folders — they appear on screen automatically.

![Python 3](https://img.shields.io/badge/python-3.8%2B-blue)
![No Dependencies](https://img.shields.io/badge/dependencies-none-green)

<video src="https://github.com/user-attachments/assets/56734454-4768-47b0-ad73-09c110e9d6fd" autoplay loop muted playsinline width="100%"></video>

## Quick Start

```bash
python3 server.py
# Open http://localhost:8080 in a full-screen browser
```

Press **F** in the browser to enter full-screen mode.

## How It Works

```
showcase/
├── index.html        ← Display page (don't edit)
├── server.py         ← Run this to start the server
├── README.md
├── photos/           ← Drop image files here
│   ├── exoskeleton-demo.jpg
│   └── robot-arm-setup.png
├── videos/           ← Drop video files here
│   └── ur12e-teleoperation.mp4
└── words/            ← Drop .txt descriptions here
    ├── exoskeleton-demo.txt
    ├── robot-arm-setup.txt
    └── ur12e-teleoperation.txt
```

### Adding Content (3 Steps)

1. **Drop your media file** into `/photos/` or `/videos/`
2. **Create a `.txt` file** in `/words/` with the **same filename** as your media
3. **Wait ~2 minutes** (or refresh the browser) — the new slide appears

**The filename becomes the on-screen title.** Hyphens and underscores are converted to spaces and title-cased automatically:

| Filename | Displayed Title |
|---|---|
| `exoskeleton-demo.jpg` | Exoskeleton Demo |
| `ur12e_teleoperation.mp4` | Ur12e Teleoperation |
| `turtlebot-navigation.png` | Turtlebot Navigation |

## Server Options

| Flag | Default | Description |
|---|---|---|
| `-title` | `"Lab Showcase"` | Display name shown in the top-left corner |
| `-time` | `8` | Seconds each photo slide is shown |
| `-port` | `8080` | Server port number |

### Examples

```bash
# Basic — default settings
python3 server.py

# Custom title and slower slides
python3 server.py -title "ECE Robotics Lab" -time 12

# Course-specific showcase
python3 server.py -title "EECE 5552 · Assistive Robotics" -time 6

# Different port
python3 server.py -title "Lab Open House" -time 10 -port 9090
```

## Keyboard Controls

These work when the browser window is focused:

| Key | Action |
|---|---|
| `Space` or `P` | Pause / Resume |
| `→` or `N` | Next slide |
| `←` or `B` | Previous slide |
| `F` | Toggle full-screen |
| Click / Tap | Pause / Resume |

## Supported Formats

| Type | Extensions |
|---|---|
| Photos | `.jpg` `.jpeg` `.png` `.gif` `.webp` `.bmp` |
| Videos | `.mp4` `.webm` `.mov` `.ogg` |
| Descriptions | `.txt` (UTF-8 plain text) |

## Tips

- **Keep filenames simple** — lowercase with hyphens works best (e.g., `mobile-robot-demo.jpg`). Avoid spaces and special characters.
- **Videos auto-play muted.** The slide advances when the video ends. Keep clips short (15–60 seconds) for the best pacing.
- **Two screens?** Open two browser tabs/windows pointing to the same `http://localhost:8080`. They cycle independently.
- **Remote access** — If the server machine is on a Tailscale network, other devices can reach it at `http://<tailscale-ip>:8080`.
- **Auto-refresh interval** — The page re-scans for new files every 2 minutes. This can be adjusted in the `CONFIG.refreshMinutes` value inside `index.html`.
- **No description file?** That's fine — the slide will just show the title with no description text.

## Requirements

- **Python 3.8+** (no pip packages needed)
- **A modern web browser** (Chrome, Firefox, Safari, Edge)
- No internet connection required — everything runs locally
