from greeclimate.device_factory import create_device
from greeclimate.device import TemperatureUnits, Mode
from ipaddress import IPv4Address
from greeclimate.discovery import Discovery
from drivers.base_device import BaseDevice

class GreeAirCondition(BaseDevice):
    def __init__(self, device_id, dev_type, ip):
        super().__init__(device_id, dev_type, ip)


        self.discovery = Discovery()
        devices = self.discovery.scan(
            wait_for=5, target_addresses=[IPv4Address(self.ip)]
        )

        self.device = create_device(devices[0])

    async def connect(self):
       await self.device.bind()

    async def turn_on(self):
        await self.device.power = True
        await self.device.push_state_update()

        return f"Successfully turned on the device: {self.device_id}"

    async def turn_off(self):
        await self.device.power = False
        await self.device.push_state_update()

        return f"Successfully turned on the device: {self.device_id}"

    async def set_temperature(self, value:int):
        await self.device.temperature_units = TemperatureUnits.C
        await self.device.target_temperature = value
        await self.device.push_state_update()

        return f"Succesfully set the temperature on the device: {self.device_id}"

    async def set_mode(self, value:str):
        modes = ["cool", "heat", "dry", "auto"]

        if value not in modes:
            raise ValueError(f"Άγνωστο mode: {value}") 

        self.device.mode = Mode.Cool if value == "cool" else Mode.Heat if value == "heat" else Mode.Auto if value == "auto" else Mode.Dry if value == "dry" else None

        self.device.push_state_update()
        return f"Succesfully set the mode on the device: {self.device_id}"


    async def get_state(self):
       
        self.device.update_state()
        return {
            "online": True,
            "power": self.device.power == "ON",
            "target_temp": self.device.target_temperature,
            "mode": self.device.mode
        }
