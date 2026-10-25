from drivers.base_device import BaseDevice
from tapo import ApiClient
from dotenv import load_dotenv
import os

load_dotenv("cfg/.env")


class TapoLight(BaseDevice):

  def __init__(self, device_id: str, device_obj, ip_address: str, tapo_username: str, tapo_password: str):
    super().__init__(device_id, ip=ip_address, dev_type= self.dev_type)
    self.device = device_obj
    self.ip_address = ip_address
    self.tapo_username = tapo_username
    self.tapo_password = tapo_password
  @classmethod
  async def create(cls, device_id: str, ip_address: str, dev_type: str, tapo_username: str, tapo_password: str):


    client = ApiClient(tapo_username, tapo_password)
    if dev_type == "tapo_l900":
      device_obj = await client.l900(ip_address)
    elif dev_type == "tapo_l920":
      device_obj = await client.l920(ip_address)
    elif dev_type == "tapo_l930":
      device_obj = await client.l930(ip_address)
    elif dev_type == "tapo_l530":
      device_obj = await client.l530(ip_address)
    elif dev_type == "tapo_l535":
      device_obj = await client.l535(ip_address)
    elif dev_type == "tapo_l510":
      device_obj = await client.l510(ip_address)
    elif dev_type == "tapo_l630":
      device_obj = await client.l630(ip_address)
    elif dev_type == "tapo_l610":
      device_obj = await client.l610(ip_address)

    return cls(device_id, device_obj, ip_address, tapo_username, tapo_password)

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