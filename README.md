# AetherOS

AetherOS is a local-first IoT hub designed for local device orchestration, automation, and control. Built with FastAPI, Python, and modern multi-brand device drivers.

---

## Features

- **Local-First Architecture:** Complete privacy and local control without relying on external cloud servers.
- **Multi-Brand Support:** 
  - Smart lights (Tapo & Yeelight with full color and brightness control).
  - Smart plugs (Tapo models: `tapo_p100`, `tapo_p110`, `tapo_p115`).
- **Interactive CLI:** Built with `questionary` for guided device registration and server management.
- **FastAPI Backend:** Robust REST API endpoints for seamless device control and event handling (`/api/light/control`, `/api/plug/control`).
- **Event Bus System:** Track and publish device triggers and state changes in real time.
- **Standalone Executable:** Ready-to-use binary package for execution on Windows.

---

## Download Release

You can download the latest standalone binary and release assets directly from the official releases page:
[AetherOS Releases](https://github.com/travletothefurureprogramming/AetherOS/releases)

---

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI, Uvicorn
- **CLI & UI:** Questionary
- **Device Libraries:** `pytapo`, `python-yeelight`, `pydantic`, `requests`

---

## Project Structure

```text
AetherOS/
├── cfg/                 # Auto-generated configuration & device registry (devices.json)
├── static/              # Frontend assets and web dashboard files
├── aetheros.py          # Main CLI management tool
├── main.py              # FastAPI application core & endpoints
└── requirements.txt     # Python dependencies
```

---

## Getting Started (From Source)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/travletothefurureprogramming/AetherOS.git
   cd AetherOS
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the AetherOS CLI:**
   ```bash
   python aetheros.py
   ```

4. **Follow the interactive menu** to register your smart devices and start the local API server.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.