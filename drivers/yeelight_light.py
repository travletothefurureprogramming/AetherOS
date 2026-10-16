from yeelight.aio import AsyncBulb
from drivers.base_device import BaseDevice



class Yeelight_Light(BaseDevice):
    def __init__(self, device_id:str, ip:str,  dev_type:str):
        super().__init__(device_id)
        self.device_id = device_id
        self.dev_type = dev_type
        self.bulb = AsyncBulb(ip)

    async def turn_on(self) -> str:
        try:
            await self.bulb.async_turn_on()
            print(f"Η συσκευή ενεργοποιήθηκε επιτυχώς: {self.device_id}")
            return f"Successfully turned on the device: {self.device_id}"
        except Exception as e:
            return f"Error while trying to turn off the {self.device_id}: {e}"


    async def turn_off(self):
        try:
            await self.bulb.async_turn_off()
            print(f"Η συσκευή απενεργοποιήθηκε επιτυχώς: {self.device_id}")
            return f"Successfully turned off the device: {self.device_id}"

        except Exception as e:
            print(f"Σφάλμα κατά την απενεργοποίηση του {self.device_id}: {e}")
            return f"Error while trying to turn off the {self.device_id}: {e}"

    async def set_colour(self, colour: str):        
        color_map = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "white": (255, 255, 255),
            "yellow": (255, 255, 0),
            "purple": (128, 0, 128),
            "orange": (255, 165, 0),
            "cyan": (0, 255, 255),
            "pink": (255, 192, 203)
        }
        
        try:
            colour_lower = colour.lower().strip()
            
            if colour_lower in color_map:
                r, g, b = color_map[colour_lower]
            elif colour_lower.startswith("#"):
                hex_color = colour_lower.lstrip('#')
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
            else:
                raise ValueError(f"Άγνωστο χρώμα: {colour}")

            await self.bulb.async_set_rgb(r, g, b)
            print(f"To χρώμα της λάμπας άλλαξε σε {colour_lower} (RGB: {r}, {g}, {b})")
            return f"The color of the lamp changed to {colour_lower}"
            
        except Exception as e:
            print(f"Σφάλμα κατά τον ορισμό χρώματος {colour}: {e}")
            return f"Error while defining color {colour}: {e}"

    async def set_brightness(self, level:int):
        try:
            await self.bulb.set_brightness(level)
            print(f"Η φωτεινότητα της λάμπας άλλαξε σε {level}%")
            return f"The brightness of the lamp set to {level}%"

        except Exception as e:
            print(f"Σφάλμα κατά τον ορισμό της φωτεινότητας σε {level}%: {e}")
            return f"Error while set the brightness to {level}%: {e}"
