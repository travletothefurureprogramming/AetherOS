from pydantic import BaseModel, Field
from typing import Literal, Union

class DeviceState(BaseModel):
    device_id: str
    is_online: bool
    current_status: str
    battery_level: int | None = Field(default=None, ge=0, le=100)

class ControlLightDevice(BaseModel):
    device_id: str
    action: Literal["turn_on", "turn_off", "set_colour", "set_brighness"]
    value: Union[str, int, None] = Field(default=None)
    triggered_by: str = Field(default="user")

class ControlTVDevice(BaseModel):
    device_id: str
    action: Literal["turn_on", "turn_off", "set_volume", "volume_up", "volume_down"]
    value: Union[int, None] = Field(default=None)
    triggered_by: str = Field(default="user")

