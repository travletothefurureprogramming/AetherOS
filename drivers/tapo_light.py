from drivers.base_device import BaseDevice
from tapo import ApiClient
from tapo.requests import Color
from common import require_env_vars

class TapoLight(BaseDevice):
    def __init__(self, device_id: str):
        super().__init__(device_id)
        tapo_username, tapo_password, self.ip_address = require_env_vars(
            "TAPO_USERNAME", "TAPO_PASSWORD", "IP_ADDRESS"
        )

        self.client = ApiClient(tapo_username, tapo_password)

    async def turn_on(self) -> str:
        return f"Succesfully turn on the device: {self.device_id}"

    async def turn_off(self) -> str:
        return f"Succesfully turn off the device: {self.device_id}"

    async def set_brightness(self, level: int) -> str:
        return f"Light {self.device_id} brightness set to {level}%"

    async def set_colour(self, colour: str) -> str:
        return f"Light {self.device_id} colour set to {colour}%"