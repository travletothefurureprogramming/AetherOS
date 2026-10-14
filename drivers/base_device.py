from abc import ABC, abstractmethod

class BaseDevice(ABC):
    def __init__(self, device_id: str):
        self.device_id = device_id

    @abstractmethod
    async def turn_on(self) -> None:
        pass

    @abstractmethod
    async def turn_off(self) -> None:
        pass