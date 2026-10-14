class EventBus:

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name: str, callback) -> bool:
        if event_name in self.subscribers:
            self.subscribers[event_name].append(callback)
            return True

        else:
            self.subscribers[event_name] = [callback]

    def publish(self, event_name: str, data: dict):
        if event_name in self.subscribers:
            for func in self.subscribers[event_name]:                
                func(data)

    def get_subscribers(self):
        return self.subscribers


if __name__ == "__main__":
    event_bus = EventBus()

    def my_listener(data):
        print(f"Το φως άναψε! Δεδομένα: {data}")

    event_bus.subscribe("light_turned_on", my_listener)
    event_bus.publish("light_turned_on", {"device_id": "light_1", "status": "on"})