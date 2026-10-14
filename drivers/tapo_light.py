from drivers.base_device import BaseDevice

class TapoLight(BaseDevice):
    def __init__(self, device_id: str):
        super().__init__(device_id)

    def turn_on(self) -> str:
        return f"Succesfully turn on the device: {self.device_id}"

    def turn_off(self) -> str:
        return f"Succesfully turn off the device: {self.device_id}"

    def set_brightness(self, level: int) -> str:
        return f"Light {self.device_id} brightness set to {level}%"

    def set_colour(self, colour: str) -> str:
        return f"Light {self.device_id} colour set to {colour}%"