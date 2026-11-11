# READ ME FIRST - AetherOS v1.0.1 Quickstart Guide

Welcome to AetherOS v1.0.1 Stable! This guide will help you install and start your local-first smart home hub.

AetherOS now provides two installation methods depending on your operating system:

- **Windows:** Standalone executables. No separate Python installation required.
- **Linux:** Source code installation with Docker and Docker Compose.

---

## Windows Installation

Windows users can install and run AetherOS without manually configuring Python or installing dependencies.

### Step 1: Download and Extract

1. Download the `v1.0.1.zip` release package from GitHub.
2. Extract the ZIP archive to your preferred location.
3. You should find the following files:

```text
AetherOS/
├── static/
├── main.exe
└── setup.exe
```

### Step 2: Initial Setup

Run:

```text
setup.exe
```

This executable handles the initial setup process.

### Step 3: Launch AetherOS

After completing the setup, run:

```text
main.exe
```

The AetherOS application will start without requiring a separate Python installation.

---

## Linux Installation (Docker)

Linux users should install AetherOS from the source code and use Docker for deployment and application startup.

### Step 1: Get the Source Code

Download the source code from the GitHub repository or clone it:

```bash
git clone https://github.com/travletothefurureprogramming/AetherOS.git
cd AetherOS
```

Make sure Docker and Docker Compose are installed on your system.

### Step 2: Start the Container

The repository includes a pre-configured Dockerfile and docker-compose.yml. No manual file creation or configuration is required before starting.

**Option A: Using Docker Compose (Recommended)**

Run the following command in the repository root:

```bash
docker compose up -d
```

**Option B: Building and Running via Docker CLI**

If you prefer to build and run the image manually:

```bash
# 1. Build the Docker image
docker build -t aetheros-hub:v1.0.1 .

# 2. Start the container
docker run -d \
  --name aetheros-hub \
  -p 8080:8080 \
  -v $(pwd)/cfg:/app/cfg \
  --restart unless-stopped \
  aetheros-hub:v1.0.1
```

### Step 3: Interactive Setup via CLI

AetherOS includes an interactive CLI that automatically handles configuration files (`cfg/devices.json`, `cfg/api_key.json`, and related setup).

To run the interactive CLI setup inside the running container:

```bash
docker exec -it aetheros-hub python aetheros.py
```

Follow the on-screen prompts to register your devices and configure the system.

### Step 4: Where to Find Your API Key

AetherOS automatically generates a unique API Key during its first initialization.

You can retrieve it using either method:

**Method 1: From the persistent configuration file**

```bash
cat cfg/api_key.json
```

**Method 2: From Docker Logs**

```bash
docker logs aetheros-hub
```

Look for the following log line:

```text
[AetherOS Security] Generated new API Key: aether_...
```

### Step 5: Access the Web Dashboard

1. Open your browser and navigate to:

   `http://localhost:8080`

   For remote access, use:

   `http://<SERVER-IP>:8080`

2. A security modal will appear requesting your API Key.
3. Paste the key retrieved in Step 4.
4. Click **Save & Connect**.

The key is saved in your browser's `localStorage` for future visits.

---

## Summary Checklist

| Task | Windows | Linux |
|---|---|---|
| Installation | Extract ZIP | Download source code |
| Initial Setup | `setup.exe` | Docker CLI |
| Start Application | `main.exe` | `docker compose up -d` |
| Interactive CLI | Included in Windows setup | `docker exec -it aetheros-hub python aetheros.py` |
| API Key | Application setup | `cfg/api_key.json` or Docker logs |
| Dashboard | `http://localhost:8080` | `http://localhost:8080` |

---

## Important Notes

- Windows users do not need to install Python separately.
- Both Windows executables are included in the official v1.0.1 ZIP package.
- Linux users must use the source code and Docker-based deployment.
- Docker Compose is the recommended deployment method for Linux.
- Configuration files and API keys are automatically generated during initialization.

