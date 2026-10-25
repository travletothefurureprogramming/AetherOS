from roku import Roku
from drivers.base_device import BaseDevice
import requests


class RokuTV(BaseDevice):
    def __init__(self, device_id, dev_type, ip):
        super().__init__(device_id, dev_type, ip)

        self.device = Roku(self.ip)

    def turn_on(self):
        self.device.home()
        return  f"Successfully turned on the device: {self.device_id}"

    def volume_up(self):
        requests.post(f"http://{self.ip}:8060/keypress/VolumeUp")
        return f"Successfully volume up the device: {self.device_id}"

    def volume_down(self):
        requests.post(f"http://{self.ip}:8060/keypress/VolumeDown")
        return f"Successfully volume down the device: {self.device_id}"

    def play(self):
        self.device.play()
        return  f"Successfully play media on the device: {self.device_id}"

    def pause(self):
        self.device.pause()
        return f"Successfully pause media on the device: {self.device_id}"

    def stop(self):
        # !!!!!! For now stop is pause !!!!!
        self.device.pause()
        return  f"Successfully stop media on the device: {self.device_id}"

    def turn_off(self):
        try:
            requests.post(f"http://{self.ip}:8060/keypress/PowerOff")
            return  f"Successfully turned off the device: {self.device_id}"
        except Exception:
            pass
