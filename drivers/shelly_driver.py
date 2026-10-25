import ShellyPy
from drivers.base_device import BaseDevice

class Shelly(BaseDevice):
    def __init__(self, device_id, dev_type, ip, relay):
        super().__init__(device_id, dev_type, ip)

        self.relay = relay
        self.device = ShellyPy.Shelly(self.ip)

    async def turn_on(self):
        self.device.relay(self.relay, turn=True)
        return  f"Successfully turned on the device: {self.device_id}"

    async def turn_off(self):
        self.device.relay(self.relay, turn=False)
        return  f"Successfully turned off the device: {self.device_id}"
