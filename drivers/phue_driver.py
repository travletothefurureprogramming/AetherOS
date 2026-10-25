from phue import Bridge
from drivers.base_device import BaseDevice

class Phue(BaseDevice):
    def __init__(self, device_id, dev_type, ip, device_number):
        super().__init__(device_id, dev_type, ip)
        self.device_number = device_number
        self.device = Bridge(ip)
        self.connect()

    def connect(self):
        self.device.connect()

    def turn_on(self):
        self.device.set_light(self.device_number, 'on', True)
        return super().turn_on()

    def turn_off(self):
        self.device.set_light(self.device_number, 'on', False)
        return super().turn_off()

