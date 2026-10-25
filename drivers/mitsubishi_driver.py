import mitsubishi_echonet as mit
from drivers.base_device import BaseDevice


class MitsubishiAirCondition(BaseDevice):
    def __init__(self, device_id, dev_type, ip):
        super().__init__(device_id, dev_type, ip)


        self.device = mit.HomeAirConditioner(netif=ip)

    def turn_on(self):
        self.device.update()
        self.device.on()

        return f"Successfully turned on the device: {self.device_id}"

    def turn_off(self):
        self.device.update()
        self.device.off()

        return f"Successfully turned on the device: {self.device_id}"

    def set_temperature(self, value:int):
        self.device.update()
        self.device.setOperationalTemperature(value)

        return f"Succesfully set the temperature on the device: {self.device_id}"

    def set_mode(self, value:str):
        modes = ["cool", "heat", "dry", "auto"]

        if value not in modes:
            raise ValueError(f"Άγνωστο mode: {value}") 

        self.device.update()

        self.device.setMode(value)
        return f"Succesfully set the mode on the device: {self.device_id}"


