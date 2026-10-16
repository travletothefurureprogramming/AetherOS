from pydantic import BaseModel, Field
from typing import Literal, Union

class DeviceState(BaseModel):
    device_id: str
    is_online: bool
    current_status: str
    battery_level: int | None = Field(default=None, ge=0, le=100)

class ControlLightDevice(BaseModel):
    device_id: str
    dev_type: Literal[
        # --- Tapo Devices ---
        "tapo_l530",
        "tapo_l535",
        "tapo_l510",
        "tapo_l630",
        "tapo_l610",
        "tapo_l900",
        "tapo_l920",
        "tapo_l930",
        # --- Yeelight Devices ---
        "yee_mono",
        "yee_mono1",
        "yee_mono5",
        "yee_monob",
        "yee_color",
        "yee_color1",
        "yee_color2",
        "yee_color4",
        "yee_color5",
        "yee_colorc",
        "yee_strip1",
        "yee_strip2",
        "yee_strip4",
        "yee_strip6",
        "yee_rgbw",
        "yee_lamp1",
        "yee_lamp3",
        "yee_lamp4",
        "yee_lamp15",
        "yee_bslamp1",
        "yee_bslamp2",
        "yee_bslamp3",
        "yee_ceiling1",
        "yee_ceiling2",
        "yee_ceiling3",
        "yee_ceiling4",
        "yee_ceiling5",
        "yee_ceiling6",
        "yee_ceiling10",
        "yee_ceiling13",
        "yee_ceiling15",
        "yee_ceiling18",
        "yee_ceiling19",
        "yee_ceiling20",
        "yee_ceiling24",
        "yee_ceil26",
        "yee_ceila",
        "yee_ceilc",
        "yee_ct_bulb",
        "yee_ct2",
    ]  
    action: Literal["turn_on", "turn_off", "set_colour", "set_brightness"]
    value: Union[str, int, None] = Field(default=None)
    triggered_by: str = Field(default="user")

class ControlPlugDevice(BaseModel):
    device_id: str
    dev_type: Literal[
        "p100", 
        "p110", 
        "p115"
        ]
    action: Literal["turn_on", "turn_off"]
    triggersd_by: str = Field(default="user")

class ControlTVDevice(BaseModel):
    device_id: str
    action: Literal["turn_on", "turn_off", "set_volume", "volume_up", "volume_down"]
    value: Union[int, None] = Field(default=None)
    triggered_by: str = Field(default="user")


