import os
from fastapi import FastAPI, HTTPException
from drivers.tapo_light import TapoLight
from models.device_models import ControlLightDevice
from core.event_bus import EventBus

app = FastAPI()
event_bus = EventBus()

devices_db = {}


@app.post("/api/light/control")
async def control_light(command: ControlLightDevice):
    device_id = command.device_id
    dev_type = command.dev_type
    action = command.action
    value = command.value
    triggered_by = command.triggered_by

    if device_id not in devices_db:
        ip_address = os.getenv("IP_ADDRESS")

        if not ip_address:
            raise HTTPException(
                status_code=500, detail="IP address not configured for device"
            )

        try:
            devices_db[device_id] = await TapoLight.create(device_id, ip_address, dev_type)
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"Could not connect to physical device {device_id}: {str(e)}",
        )

        device = devices_db[device_id]

        if action == "turn_on":
            await device.turn_on()
        elif action == "turn_off":
            await device.turn_off()
        elif action == "set_colour":
            await device.set_colour(value)
        elif action == "set_brighness":
            await device.set_brightness(value)
        else:
            raise HTTPException(status_code=400, detail="Unknown action")

        await event_bus.publish(
            f"{device_id}_{action}",
            {
            "device_id": device_id,
            "dev_type": dev_type,
            "action": action,
            "value": value,
            "triggered_by": triggered_by,
        },)
  

        return {
            "status": "success",
            "message": f"Executed {action} on {device_id}",
        }