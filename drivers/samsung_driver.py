import logging
import os
from drivers.base_device import BaseDevice
from samsungtvws import SamsungTVWS  

logging.basicConfig(level=logging.INFO)


class SamsungTV(BaseDevice):
    def __init__(self, device_id:str, dev_type:str, ip:str):
        super().__init__(device_id)
        self.device_id = device_id
        self.dev_type = dev_type
        self.ip = ip

        token_file = os.path.join("cfg", f"samsung_{device_id}.txt")
        self.tv = SamsungTVWS(host=self.ip, port=8002, token_file=token_file)


    def turn_on(self):
        self.tv.shortcuts().power()
        return  f"Successfully turned on the device: {self.device_id}"

    def turn_off(self):
        self.tv.shortcuts().power()
        return  f"Successfully turned off the device: {self.device_id}"

    def volume_up(self):
        self.tv.shortcuts().volume_up()
        return f"Successfully volume up the device: {self.device_id}"

    def volume_down(self):
        self.tv.shortcuts().volume_down()
        return f"Successfully voulume down the device: {self.device_id}"
    
    def play(self):
        self.tv.send_key("KEY_PLAY")
        return  f"Successfully play media on the device: {self.device_id}"
    
    def pause(self):
        self.tv.send_key("KEY_PAUSE")
        return f"Successfully pause media on the device: {self.device_id}"
    
    def select_source(self, source: str):
        self.tv.run_app(source)
        return  f"Successfully change source on the device: {self.device_id}"
