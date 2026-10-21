# Changelog

All notable changes to AetherOS will be documented in this file.

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
