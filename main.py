import json
import os
import socket
import uvicorn
from core.event_bus import EventBus
from drivers.tapo_light import TapoLight
from drivers.lg_driver import WebOSTv
from drivers.samsung_driver import SamsungTV
from drivers.shelly_driver import Shelly
from drivers.phue_driver import Phue
from drivers.tapo_plug import TapoPlug
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from models.device_models import ControlLightDevice, ControlPlugDevice, ControlTVDevice, ControlAirConditionDevice
from fastapi.responses import FileResponse
from drivers.yeelight_light import Yeelight_Light
from drivers.wiz_driver import WizLight
from drivers.daikinac_driver import DaikinAc

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
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

def get_local_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
  except Exception:
    local_ip = "127.0.0.1"
  finally:
    s.close()
  return local_ip

@app.get("/")
async def serve_dashboard():
    return FileResponse("static/index.html")

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

  if "shelly" in dev_type.lower() or brand == "Shelly":
    relay_number = device_config.get("relay")

  if "phue" in dev_type.lower() or brand == "Phue":
    device_number = device_config.get("number")

  if device_id not in devices_db:
    if brand == "Yeelight" or dev_type.startswith("yee_"):
      try:
        devices_db[device_id] = Yeelight_Light(device_id, ip_address, dev_type)
      except Exception as e:
        print(f"Could not connect to physical device {device_id}: {str(e)}")
        raise HTTPException(
          status_code=502,
          detail=f"Could not connect to physical device {device_id}: {str(e)}",
        )
    elif brand == "Shelly" or dev_type.startswith("shell_"):
      try:
        devices_db[device_id] = Shelly(device_id,dev_type, ip_address, relay_number)
      except Exception as e:
        print(f"Could not connect to physical device {device_id}: {str(e)}")
        raise HTTPException(
          status_code=502,
          detail=f"Could not connect to physical device {device_id}: {str(e)}",
        )
    elif brand == "Phue" or dev_type.startswith("phue_"):
      try:
        devices_db[device_id] = Phue(device_id,dev_type, ip_address, device_number)
      except Exception as e:
        print(f"Could not connect to physical device {device_id}: {str(e)}")
        raise HTTPException(
          status_code=502,
          detail=f"Could not connect to physical device {device_id}: {str(e)}",
        )
    elif brand == "Wiz" or dev_type.startswith("wiz_"):
      try:
        devices_db[device_id] = WizLight(device_id, dev_type, ip_address)
      except Exception as e:
        print(f"Could not connect to physical device {device_id}: {str(e)}")
        raise HTTPException(
          status_code=502,
          detail=f"Could not connect to physical device {device_id}: {str(e)}",
        )
    else:
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
        if brand == "Tapo":
          devices_db[device_id] = await TapoLight.create(
              device_id, ip_address, dev_type, email, password
          )
        elif brand == "Shelly":
          devices_db[device_id] = Shelly(device_id, dev_type, ip_address, relay_number)
        elif brand == "Yeelight":
          devices_db[device_id] = Yeelight_Light(device_id, ip_address, dev_type)
        elif brand == "Phue":
          devices_db[device_id] = Phue(device_id, dev_type, ip_address, device_number)
        elif brand == "Wiz":
          devices_db[device_id] = WizLight(device_id, dev_type, ip_address)

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

@app.post("/api/plug/control")
async def control_plug(command: ControlPlugDevice):
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
    if dev_type.lower() in ["tapo_p100", "tapo_p110", "tapo_p115"] or "tapo" in dev_type.lower():        
        try:
          devices_db[device_id] = await TapoPlug.create(
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
    else:
      raise HTTPException(status_code=400, detail="Unknown action")

  except Exception as e:
    error_str = str(e)
    if "SESSION_TIMEOUT" in error_str or "Unauthorized" in error_str:
      if device_id in devices_db:
        del devices_db[device_id]
      
      try:
        devices_db[device_id] = await TapoPlug.create(
            device_id, ip_address, dev_type, email, password
        )
        device = devices_db[device_id]
        
        if action == "turn_on":
          await device.turn_on()
        elif action == "turn_off":
          await device.turn_off()
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

@app.post("/api/tv/control")
async def control_tv(command: ControlTVDevice):
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

  if device_id not in devices_db:
    if "lg" in dev_type.lower() or brand in ["Lg", "LG"]:        
        try:
          tv_instance = WebOSTv(device_id, ip_address, dev_type)
          await tv_instance.connect()
          devices_db[device_id] = tv_instance
        except Exception as e:
          raise HTTPException(status_code=502, detail=f"Could not connect to LG TV {device_id}: {str(e)}")
          
    elif "samsung" in dev_type.lower() or brand in ["Samsung", "samsung"]:
        try:
          devices_db[device_id] = SamsungTV(device_id, ip_address, dev_type)
        except Exception as e:
          raise HTTPException(status_code=502, detail=f"Could not connect to Samsung TV {device_id}: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail=f"Unknown TV brand/type: {brand}")

  device = devices_db[device_id]

  try:
    if brand in ["Lg", "LG"] or "lg" in dev_type.lower():
      if action == "turn_on":
          await device.turn_on()
      elif action == "turn_off":
          await device.turn_off()
      elif action == "play":
          await device.play()
      elif action == "pause":
          await device.pause()
      elif action == "stop":
          await device.stop()
      elif action == "volume_up":
          await device.volume_up()
      elif action == "volume_down":
          await device.volume_down()
      elif action == "fast_forward":
          await device.fast_forward()
      elif action == "rewind":
          await device.rewind()
      elif action == "select_source":
          await device.select_source(value)
      else:
          raise HTTPException(status_code=400, detail="Unknown action")
          
    else: 
      if action == "turn_on":
          device.turn_on()
      elif action == "turn_off":
          device.turn_off()
      elif action == "play":
          device.play()
      elif action == "pause":
          device.pause()
      elif action == "stop":
          device.stop()
      elif action == "volume_up":
          device.volume_up()
      elif action == "volume_down":
          device.volume_down()
      elif action == "select_source":
          device.select_source(value)
      else:
          raise HTTPException(status_code=400, detail="Unknown action")

  except Exception as e:
    if device_id in devices_db:
      del devices_db[device_id]
    raise HTTPException(status_code=500, detail=f"TV execution error: {str(e)}")

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

@app.get("/api/air-condition/state/{device_id}")
async def get_state(device_id):
  try:
    device_config = get_device_from_registry(device_id)
    if not device_config:
      raise HTTPException(
          status_code=404,
          detail=f"Device '{device_id}' not found in registry. Please register it first.",
      )

    dev_type = device_config.get("device_type")
    ip_address = device_config.get("ip_address")
    brand = device_config.get("brand")

    if device_id not in devices_db:
      if brand == "Daikin" or dev_type.startswith("daikin_"):
        devices_db[device_id] = DaikinAc(device_id, dev_type, ip_address)

    device = devices_db[device_id]

    return device.get_state()
  except Exception as e:
    return f"An error has occured: {e}"

@app.post("/api/air-condition/control")
async def control_air_condition(command: ControlAirConditionDevice):
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

  if device_id not in devices_db:
    if brand == "Daikin" or dev_type.startswith("daikin_"):
      devices_db[device_id] = DaikinAc(device_id, dev_type, ip_address)

  device = devices_db[device_id]
  try:
    if action == "turn_on":
      device.turn_on()
    elif action == "turn_off":
      device.turn_off()
    elif action == "set_mode":
      device.set_mode(value)
    elif action == "set_temperature":
      device.set_temperature(value)
  except Exception as e:
    error_str = str(e)
    if "SESSION_TIMEOUT" in error_str or "Unauthorized" in error_str:
      if device_id in devices_db:
        del devices_db[device_id]
      
      try:
        if brand == "Daikin" or dev_type.startswith("daikin_"):
          devices_db[device_id] = DaikinAc(device_id, dev_type, ip_address)

        device = devices_db[device_id]

        if action == "turn_on":
          device.turn_on()
        elif action == "turn_off":
          device.turn_off()
        elif action == "set_mode":
          device.set_mode(value)
        elif action == "set_temperature":
          device.set_temperature(value)

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

  print(f"\n[🚀] Starting Uvicorn Server on http://127.0.0.1:8080 and http://{get_local_ip()}:8080 ...")
  uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
  main()