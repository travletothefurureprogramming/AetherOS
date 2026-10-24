# Changelog

All notable changes to AetherOS will be documented in this file.

## [0.8.0-alpha] - 2026-10-24
### Added
- **Mitsubishi AC Integration**: Added local Echonet Lite driver support for Mitsubishi-based mini-split air conditioners.
- **Climate Control Handlers**: Implemented asynchronous state management for power states, operating modes, and target temperatures.
- **Manual IP Setup & CLI Expansion**: Updated backend routing endpoints and extended the interactive setup wizard (`aetheros.py`) to support direct manual static IP registration for Mitsubishi devices.

## [0.7.0-alpha] - 2026-10-24
### Added
- **Gree AC Integration**: Added local UDP driver support (port 7000) for Gree-based mini-split air conditioners and OEM equivalents (e.g., Inventor, Cooper&Hunter, Carrier).
- **Climate Control Handlers**: Implemented asynchronous state management for power states, operating modes (cool, heat, auto, dry, fan), target temperatures, and fan speeds.
- **Manual IP Setup & CLI Expansion**: Updated `main.py` routing endpoints and extended the interactive setup wizard (`aetheros.py`) to support direct manual static IP registration for Gree devices.

## [0.6.0-alpha] - 2026-10-24
### Added
- **Roku TV Integration**: Added local ECP driver support (port 8060) for Roku media players and Smart TVs.
- **Extended HTTP Protocol Controls**: Implemented direct HTTP POST endpoints for volume control (VolumeUp, VolumeDown, VolumeMute) and power management (PowerOff).
- **Setup Wizard Expansion**: Updated `main.py` routing endpoints and aetheros.py CLI wizard to support Roku TV onboarding.

## [0.5.0-alpha] - 2026-10-23
### Added
- **Sony Bravia TV Integration**: Added local REST API and envelope support via `sony-bravia-api` using Pre-Shared Key (PSK) authentication.
- **Unified Input Parsing**: Implemented regex-based input string parsing in the Sony Bravia driver to seamlessly map unified API inputs (e.g., "hdmi1") to driver-level arguments.
- **CLI & Backend Expansion**: Updated `aetheros.py` wizard and `main.py` routing logic to support registering and controlling Sony Bravia smart televisions locally.

## [0.4.0-alpha] - 2026-10-21
### Added
- **WiZ Smart Lights Integration**: Added zero-config, local-first UDP driver for WiZ bulbs and light strips.
- **Daikin AC Integration**: Introduced local HTTP API support via `pydaikin` for smart climate control (power, target temperature, indoor telemetry).
- **Expanded Ecosystem**: Further consolidated local-first lighting, relay, media, and climate device routing.

## [0.3.0-alpha] - 2026-10-12
### Added
- **Shelly Integration**: Added native local HTTP support for Shelly relays and smart plugs, with custom relay number configuration via backend and interactive CLI.
- **Philips Hue Support**: Integrated comprehensive Philips Hue lighting control via the `phue` library for seamless bridge communication and specific light ID routing.
### Improved
- **CLI & Backend Enhancements**: Updated device registration wizard and core routing logic (`main.py`) to seamlessly manage multi-brand hardware from a single unified local hub.
- **Robust Error Handling**: Enhanced exception handling and connection stability across new device drivers.

## [0.2.0-alpha] - 2026-10-11
### Added
- **Samsung Smart TV Integration**: Added synchronous driver (`samsungtvws`) supporting Tizen OS models with secure local WebSocket communication (port 8002) and automated token persistence.
- **LG webOS TV Enhancements**: Refined asynchronous control flows, session management, and robust error handling.
- **CLI & Dashboard Expansion**: Updated configuration wizard to manage Samsung TVs alongside LG webOS models, lights, and smart plugs under unified API endpoints (`/api/tv/control`).
- **Distribution & Packaging**: Packaged standalone executable binary distributions (`.exe`) via PyInstaller.

## [0.1.0-alpha] - 2026-10-10
### Added
- Initial pre-release of AetherOS, a local-first IoT hub.
- Multi-brand device support (Tapo lights/plugs, Yeelight lights).
- Local FastAPI backend & CLI interface.
- Local-first architecture (`devices.json`).
