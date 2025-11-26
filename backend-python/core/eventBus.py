# backend-python/core/eventBus.py

class EventBus:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name: str, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def publish(self, event_name: str, data: dict):
        for callback in self.listeners.get(event_name, []):
            # schedule asynchronously
            import asyncio
            asyncio.create_task(callback(data))

# Singleton instance
eventBus = EventBus()
