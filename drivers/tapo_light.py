from drivers.base_device import BaseDevice
from tapo import ApiClient
from dotenv import load_dotenv
import os

load_dotenv()


class TapoLight(BaseDevice):

  def __init__(self, device_id: str, device_obj, ip_address: str):
    super().__init__(device_id)
    self.device = device_obj
    self.ip_address = ip_address

  @classmethod
  async def create(cls, device_id: str, ip_address: str):
    tapo_username = os.getenv("TAPO_USERNAME")
    tapo_password = os.getenv("TAPO_PASSWORD")

    client = ApiClient(tapo_username, tapo_password)
    device_obj = await client.l900(ip_address)

    return cls(device_id, device_obj, ip_address)

  async def turn_on(self) -> str:
    await self.device.on()
    return f"Successfully turned on the device: {self.device_id}"

  async def turn_off(self) -> str:
    await self.device.off()
    return f"Successfully turned off the device: {self.device_id}"

  async def set_brightness(self, level: int) -> str:
    await self.device.set_brightness(level)
    return f"Light {self.device_id} brightness set to {level}%"

  async def set_colour(self, colour: str) -> str:
    await self.device.set_color(colour)
    return f"Light {self.device_id} colour set to {colour}"