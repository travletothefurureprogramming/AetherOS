# AetherOS

<img width="1852" height="630" alt="Screenshot 2026-10-25 232316" src="https://github.com/user-attachments/assets/8c5d9ca2-e3f2-449d-aec0-ab82e60220fc" />


AetherOS is a local-first IoT hub designed for local device orchestration, automation, and control. Built with FastAPI, Python, and modern multi-brand device drivers.

## Features

* **Local-First Architecture:** Complete privacy and local control without relying on external cloud servers.

* **Multi-Brand Device Support:**

  * **Smart TVs:** LG, Samsung, Sony Bravia, Roku.

  * **Smart Lights:** Tapo, Yeelight, WiZ, Philips Hue (`phue`), Shelly *(color and brightness capabilities vary by model)*.

  * **Smart Plugs:** Tapo models (`tapo_p100`, `tapo_p110`, `tapo_p115`).

  * **Air Conditioners:** Daikin, Gree, Mitsubishi.

  * **Speakers:** Sonos.

* **Interactive CLI:** Built with `questionary` for guided device registration, configuration management, and server administration.

* **FastAPI Backend:** REST API endpoints secured with automatic API key authentication.

* **Event Bus System:** Real-time tracking and publishing of device state changes and triggers.

* **Standalone Executable:** Ready-to-use binary packages available for direct execution on Windows.

## Detailed Setup & Usage Guide

For complete step-by-step instructions on running the Docker container, finding your auto-generated API Key, configuring the Web UI, and using the Interactive CLI, please refer to:

[**READ_ME_FIRST.md**](READ_ME_FIRST.md)

## Download Release

You can download the latest standalone binary and release assets directly from the official releases page:
[AetherOS Releases](https://github.com/travletothefurureprogramming/AetherOS/releases)

## Tech Stack

* **Language:** Python 3.10+

* **Framework:** FastAPI, Uvicorn

* **CLI & UI:** Questionary

* **Device Libraries:** `pytapo`, `python-yeelight`, `pydantic`, `requests`

## Getting Started (From Source)

1. **Clone the repository:**

   ```
   git clone https://github.com/travletothefurureprogramming/AetherOS.git
   cd AetherOS
   
   ```

2. **Install dependencies:**

   ```
   pip install -r requirements.txt
   
   ```

3. **Run the AetherOS CLI:**

   ```
   python aetheros.py
   uvicorn main:app
   ```

4. **Follow the interactive menu** to register your smart devices and start the local API server.

## License

Distributed under the MIT License. See `LICENSE` for more information.
