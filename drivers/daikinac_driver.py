import asyncio
import logging
from drivers.base_device import BaseDevice
import aiohttp
from pydaikin.daikin_base import Appliance
from pydaikin.factory import DaikinFactory

HOST = "10.1.1.21"

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)


async def main():
    async with await DaikinFactory(HOST) as device:
        await device.update_status()
        device.show_sensors()


class DaikinAc(BaseDevice):
    def __init__(self, device_id, dev_type, ip):
        super().__init__(device_id)
        self.device_id = device_id
        self.dev_type = dev_type
        self.ip = ip

        self.device = Appliance(self.ip)

    async def turn_on(self):
        try:
            self.device.set({'mode': 'on'})
            print(f"Η συσκευή ενεργοποιήθηκε επιτυχώς: {self.device_id}")
            return f"Successfully turned on the device: {self.device_id}"

        except Exception as e:
            print(f"Σφάλμα κατά την ενεργοποίηση του {self.device_id}: {e}")
            return f"An error has occured on the device: {self.device_id}: {e}"

    async def turn_off(self):
        try:
            self.device.set({'mode':'off'})
            print(f"Η συσκευή απενεργοποιήθηκε επιτυχώς: {self.device_id}")
            return f"Successfully turned off the device: {self.device_id}"
        
        except Exception as e:
            print(f"Σφάλμα κατά την απενεργοποίηση του {self.device_id}: {e}")
            return f"An error has occured on the device: {self.device_id}: {e}"

    async def set_temperature(self, value:int):
        try:
            self.device.set({'stemp':value})
            print(f"Η θερμοκρασία της συσκευής ρυθμίστικε επιτυχώς: {self.device_id}")
            return f"Succesfully set the temperature on the device: {self.device_id}"

        except Exception as e:
            print(f"Σφάλμα κατά την ρύθμιση της θερμοκρασίας του {self.device_id}: {e}")
            return f"An error has occured on the device: {self.device_id}: {e}"

    async def set_mode(self, value:str):
        try:
            modes = ["cool", "heat", "dry", "auto"]

            if value not in modes:
                raise ValueError(f"Άγνωστο mode: {value}") 

            self.device.set({'mode':value})

            print(f"Η λειτουργεία της συσκευής ρυθμίστικε επιτυχώς: {self.device_id}")
            return f"Succesfully set the mode on the device: {self.device_id}"

        except Exception as e:
            print(f"Σφάλμα κατά την ρύθμιση της λειτουργίας του {self.device_id}: {e}")
            return f"An error has occured on the device: {self.device_id}: {e}"
            

    async def get_state(self):
        try:
            self.device.update_status()
            return {
                "online": True,
                "power": self.device.values.get("power") == "ON",
                "target_temp": self.device.values.get("temp"),
                "indoor_temp": self.device.values.get("indoor_temp"),
                "mode": self.device.values.get("mode")
            }

        except Exception as e:
            print(f"Σφάλμα κατα την έυρεση της κατάστασης του {self.device_id}")
            return f"An error has occured on the device: {self.device_id}: {e}"
