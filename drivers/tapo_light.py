from drivers.base_device import BaseDevice
from tapo import ApiClient
from tapo.requests import Color
from common import require_env_vars
import asyncio

class TapoLight(BaseDevice):
    def __init__(self, device_id: str):
        super().__init__(device_id)
        tapo_username, tapo_password, self.ip_address = require_env_vars(
            "TAPO_USERNAME", "TAPO_PASSWORD", "IP_ADDRESS"
        )

        self.client = ApiClient(tapo_username, tapo_password)

        asyncio.run(self.connect())
    
    async def connect(self):
        self.device = await self.client.l900(self.ip_address)

    async def turn_on(self) -> str:
        await self.device.on()
        return f"Succesfully turn on the device: {self.device_id}"

    async def turn_off(self) -> str:
        await self.device.off()
        return f"Succesfully turn off the device: {self.device_id}"

    async def set_brightness(self, level: int) -> str:
        await self.device.set_brightness(level)
        return f"Light {self.device_id} brightness set to {level}%"

    async def set_colour(self, colour: str) -> str:
        await self.device.set_color(colour)
        return f"Light {self.device_id} colour set to {colour}%"