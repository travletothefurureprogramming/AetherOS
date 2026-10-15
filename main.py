import json
import os
import uvicorn
from core.event_bus import EventBus
from drivers.tapo_light import TapoLight
from fastapi import FastAPI, HTTPException
from models.device_models import ControlLightDevice

app = FastAPI()
event_bus = EventBus()
devices_db = {}

CONFIG_DIR = "cfg"
DB_FILE = os.path.join(CONFIG_DIR, "devices.json")


def load_registered_devices():
  if not os.path.exists(DB_FILE):
    return []

  try:
    with open(DB_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  except json.JSONDecodeError:
    print("[!] Σφάλμα κατά την ανάγνωση του JSON.")
    return []


def get_device_from_registry(device_id: str):
  devices = load_registered_devices()
  for dev in devices:
    if dev.get("device_id") == device_id:
      return dev
  return None


@app.get("/api/devices")
async def get_devices():
  devices = load_registered_devices()
  sanitized_devices = []
  for dev in devices:
    dev_copy = dev.copy()
    if "auth" in dev_copy:
      dev_copy["auth"] = {"email": dev_copy["auth"].get("email"), "password": "[PROTECTED]"}
    sanitized_devices.append(dev_copy)
  return sanitized_devices


@app.post("/api/light/control")
async def control_light(command: ControlLightDevice):
  device_id = command.device_id
  dev_type = command.dev_type
  action = command.action
  value = command.value
  triggered_by = command.triggered_by

  device_config = get_device_from_registry(device_id)
  if not device_config:
    raise HTTPException(
        status_code=404,
        detail=f"Device '{device_id}' not found in registry. Please register it first.",
    )

  ip_address = device_config.get("ip_address")
  brand = device_config.get("brand")

  email, password = None, None
  if "tapo" in dev_type.lower() or brand == "Tapo":
    auth_data = device_config.get("auth", {})
    email = auth_data.get("email")
    password = auth_data.get("password")

  if device_id not in devices_db:
    try:
      devices_db[device_id] = await TapoLight.create(
          device_id, ip_address, dev_type, email, password
      )
    except Exception as e:
      raise HTTPException(
          status_code=502,
          detail=f"Could not connect to physical device {device_id}: {str(e)}",
      )

  device = devices_db[device_id]

  try:
    if action == "turn_on":
      await device.turn_on()
    elif action == "turn_off":
      await device.turn_off()
    elif action == "set_colour":
      await device.set_colour(value)
    elif action == "set_brightness":
      await device.set_brightness(value)
    else:
      raise HTTPException(status_code=400, detail="Unknown action")

  except Exception as e:
    error_str = str(e)
    if "SESSION_TIMEOUT" in error_str or "Unauthorized" in error_str:
      if device_id in devices_db:
        del devices_db[device_id]
      
      try:
        devices_db[device_id] = await TapoLight.create(
            device_id, ip_address, dev_type, email, password
        )
        device = devices_db[device_id]
        
        if action == "turn_on":
          await device.turn_on()
        elif action == "turn_off":
          await device.turn_off()
        elif action == "set_colour":
          await device.set_colour(value)
        elif action == "set_brightness":
          await device.set_brightness(value)
      except Exception as inner_e:
        raise HTTPException(
            status_code=502,
            detail=f"Session expired and auto-reconnect failed: {str(inner_e)}",
        )
    else:
      raise HTTPException(status_code=500, detail=f"Device error: {error_str}")

  await event_bus.publish(
      f"{device_id}_{action}",
      {
          "device_id": device_id,
          "dev_type": dev_type,
          "action": action,
          "value": value,
          "triggered_by": triggered_by,
      },
  )

  return {
      "status": "success",
      "message": f"Executed {action} on {device_id}",
  }


def main():
  print("--- AetherOS Core / API Loader ---")

  devices = load_registered_devices()

  if not devices:
    print("Καμία συσκευή δεν είναι καταχωρισμένη.")
  else:
    print(f"Βρέθηκαν συνολικά {len(devices)} συσκευές στο registry.\n")
    for device in devices:
      device_id = device.get("device_id")
      brand = device.get("brand")
      device_type = device.get("device_type")
      ip_address = device.get("ip_address")

      print(f"-> Συσκευή ID: {device_id}")
      print(f"   Μάρκα: {brand} | Τύπος: {device_type}")
      print(f"   IP Address: {ip_address}")

      if brand == "Tapo" and "auth" in device:
        email = device["auth"].get("email")
        print(f"   [Auth] Email: {email} | Password: [PROTECTED]")

      print("-" * 40)

  print("\n[🚀] Starting Uvicorn Server on http://0.0.0.0:8080 ...")
  uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
  main()