# READ ME FIRST - AetherOS v1.0.0 Quickstart Guide

Welcome to AetherOS v1.0.0 Stable. Follow this step-by-step guide to get your local-first homelab hub up and running.

## Step 1: Start the Container

The repository includes a pre-configured Dockerfile and docker-compose.yml. No manual file creation or configuration is required before starting.

### Option A: Using Docker Compose (Recommended)

Run the following command in the repository root:

```
docker compose up -d
```

### Option B: Building and Running via Docker CLI

If you prefer to build and run the image manually:

```
# 1. Build the Docker image
docker build -t aetheros-hub:v1.0.0 .

# 2. Start the container
docker run -d \
  --name aetheros-hub \
  -p 8080:8080 \
  -v $(pwd)/cfg:/app/cfg \
  --restart unless-stopped \
  aetheros-hub:v1.0.0
```

## Step 2: Interactive Setup via CLI

AetherOS includes an interactive CLI that automatically handles configuration files (`cfg/devices.json`, `cfg/api_key.json`, and all related setup). You do not need to create any files manually.

To run the interactive CLI setup inside the running container:

```
docker exec -it aetheros-hub python aetheros.py
```

Follow the on-screen prompts to add your devices and manage system configurations automatically.

## Step 3: Where to Find Your API Key

AetherOS automatically generates a unique API Key during its first initialization. You can retrieve it in two ways:

### Method 1: From the persistent config file

View the auto-generated key on your host system:

```
cat cfg/api_key.json
```

Output:

```json
{
    "api_key": "aether_a1b2c3d4e5f67890..."
}
```

### Method 2: From Docker Logs

Inspect the startup logs of the container:

```
docker logs aetheros-hub
```

Look for the following log line:
`[AetherOS Security] Generated new API Key: aether_...`

## Step 4: Access the Web Dashboard

1. Open your browser and navigate to:
   `http://localhost:8080` (or `http://<SERVER-IP>:8080` if hosted remotely)
2. A security modal will appear requesting your API Key.
3. Paste the key retrieved in Step 3 (`aether_...`).
4. Click Save & Connect. The key is saved securely in your browser's `localStorage` for future visits.

## Summary Checklist

| Task                   | Command / Location                                       |
| ---------------------- | -------------------------------------------------------- |
| Start Hub              | `docker compose up -d`                                 |
| Interactive CLI Setup  | `docker exec -it aetheros-hub python aetheros.py`      |
| View API Key           | `cat cfg/api_key.json` or `docker logs aetheros-hub` |
| Open Dashboard         | `http://localhost:8080`                                |
| Container Shell Access | `docker exec -it aetheros-hub /bin/bash`               |
