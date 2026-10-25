from abc import ABC, abstractmethod

class BaseDevice(ABC):
    def __init__(self, device_id: str, dev_type: str, ip: str):
        self.device_id = device_id
        self.dev_type = dev_type
        self.ip = ip

    @abstractmethod
    async def turn_on(self) -> None:
        pass

    @abstractmethod
    async def turn_off(self) -> None:
        pass