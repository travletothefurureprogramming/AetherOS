import os
import logging
from bscpylgtv import WebOsClient
from drivers.base_device import BaseDevice

CONFIG_DIR = "cfg"
KEY_FILE = os.path.join(CONFIG_DIR, ".aiopylgtv.sqlite")

os.makedirs(CONFIG_DIR, exist_ok=True)

class WebOSTv(BaseDevice):
    def __init__(self, device_id: str, dev_type: str, ip: str):
        super().__init__(device_id)
        self.device_id = device_id
        self.dev_type = dev_type
        self.ip = ip
        self.device: WebOsClient = None

    async def connect(self):
        try:
            self.device = await WebOsClient.create(key_file_path=KEY_FILE, ip="192.168.1.8")
            await self.device.connect()
            print(f"Επιτυχής σύνδεση με την LG TV ({self.ip})!")
            return True
        except Exception as e:
            print(f"Σφάλμα σύνδεσης στην LG TV: {e}")
            return False

    async def turn_on(self):
        if not self.device:
            await self.connect()
        await self.device.power_on()
        return f"Successfully turned on the device: {self.device_id}"

    async def turn_off(self):
        if not self.device:
            await self.connect()
        await self.device.power_off()
        return f"Successfully turned off the device: {self.device_id}"

    async def pause(self):
        if not self.device:
            await self.connect()
        await self.device.pause()
        return f"Successfully pause media on the device: {self.device_id}"

    async def play(self):
        if not self.device:
            await self.connect()
        await self.device.play()
        return f"Successfully play media on the device: {self.device_id}"

    async def volume_up(self):
        if not self.device:
            await self.connect()
        await self.device.volume_up()
        return f"Successfully volume up the device: {self.device_id}"

    async def volume_down(self):
        if not self.device:
            await self.connect()
        await self.device.volume_down()
        return f"Successfully volume down the device: {self.device_id}"

    async def select_source(self, source: str):
        if not self.device:
            await self.connect()
        await self.device.set_input(source)
        return f"Successfully set {source} on the device: {self.device_id}"