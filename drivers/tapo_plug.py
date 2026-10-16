from drivers.base_device import BaseDevice
from tapo import ApiClient
from dotenv import load_dotenv
import os

load_dotenv("cfg/.env")


class TapoPlug(BaseDevice):

  def __init__(self, device_id: str, device_obj, ip_address: str, tapo_username: str, tapo_password: str):
    super().__init__(device_id)
    self.device = device_obj
    self.ip_address = ip_address
    self.tapo_username = tapo_username
    self.tapo_password = tapo_password
  @classmethod
  async def create(cls, device_id: str, ip_address: str, dev_type: str, tapo_username: str, tapo_password: str):


    client = ApiClient(tapo_username, tapo_password)
    if dev_type == "tapo_p100":
      device_obj = await client.p100(ip_address)
    elif dev_type == "tapo_p110":
      device_obj = await client.p110(ip_address)
    elif dev_type == "tapo_p115":
      device_obj = await client.p115(ip_address)

    return cls(device_id, device_obj, ip_address, tapo_username, tapo_password)

  async def turn_on(self) -> str:
    await self.device.on()
    return f"Successfully turned on the device: {self.device_id}"

  async def turn_off(self) -> str:
    await self.device.off()
    return f"Successfully turned off the device: {self.device_id}"
