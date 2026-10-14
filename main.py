from models.device_models import ControlLightDevice
from drivers.tapo_light import TapoLight
from fastapi import FastAPI, HTTPException
from core.event_bus import EventBus

devices_db = {
    "light_1": TapoLight("light_1")
}

app = FastAPI()
event_bus = EventBus()

@app.post("/api/light/control")
async def control_light(command: ControlLightDevice):
    device_id = command.device_id
    action = command.action
    value = command.value
    triggerd_by = command.triggered_by

    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")

    if action == "turn_on":
        devices_db[device_id].turn_on()
        await event_bus.publish(f"{device_id}_{action}", {"device_id":device_id, "action":action, "value": value, "triggerd_by": triggerd_by})
    elif action == "turn_off":
        devices_db[device_id].turn_off()
        await event_bus.publish(f"{device_id}_{action}", {"device_id":device_id, "action":action, "value": value, "triggerd_by": triggerd_by})
    elif action == "set_colour":
        devices_db[device_id].set_colour(value)
        await event_bus.publish(f"{device_id}_{action}", {"device_id":device_id, "action":action, "value": value, "triggerd_by": triggerd_by})
    elif action == "set_brighness":
        devices_db[device_id].set_brightness(value)
        await event_bus.publish(f"{device_id}_{action}", {"device_id":device_id, "action":action, "value": value, "triggerd_by": triggerd_by})
