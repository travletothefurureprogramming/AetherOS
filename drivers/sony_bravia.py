from sony_bravia_api import Bravia
from drivers.base_device import BaseDevice
import re
class SonyBraviaTv(BaseDevice):
    def __init__(self, device_id, dev_type, ip, psk):
        super().__init__(device_id)
        self.device_id = device_id
        self.dev_type = dev_type
        self.ip = ip
        self.device = Bravia(device_id, ip, f'http://{ip}/sony/', psk)


    def turn_on(self):
        self.device.power(True)
        return  f"Successfully turned on the device: {self.device_id}"

    def turn_off(self):
        self.device.power(False)
        return  f"Successfully turned off the device: {self.device_id}"

    def set_volume(self, volume:int):
        self.device.setVol(str(volume))
        return f"Successfully set volume to the device: {self.device_id}"

    def volume_up(self):
        self.device.volUp()
        return f"Successfully volume up the device: {self.device_id}"

    def volume_down(self):
        self.device.volDown()
        return f"Successfully volume down the device: {self.device_id}"

    def play(self):
        self.device.play()
        return  f"Successfully play media on the device: {self.device_id}"

    def pause(self):
        self.device.pause()
        return  f"Successfully pause media on the device: {self.device_id}"

    def stop(self):
        # !!!!!! For now stop is pause !!!!!
        self.device.pause()
        return  f"Successfully stop media on the device: {self.device_id}"


    def select_source(self, source: str):

        input_str = input_str.strip().lower()
        
        match = re.match(r"^([a-z]+)(\d+)$", input_str)
        if not match:
            return {"status": "error", "message": f"Invalid input format: '{input_str}'. Use format like 'hdmi1'."}
        
        input_type, port = match.groups()
        
        if input_type == "hdmi":
            self.client.setExtInput("hdmi", port)
        elif input_type in ["video", "av"]:
            self.client.setExtInput("video", port)
        else:
            self.client.setExtInput(input_type, port)
        return  f"Successfully change source on the device: {self.device_id}"

