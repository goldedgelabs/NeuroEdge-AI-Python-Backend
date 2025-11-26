# backend-python/core/eventBus.py

import asyncio

class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name: str, callback):
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)

    def publish(self, event_name: str, data):
        for callback in self.subscribers.get(event_name, []):
            asyncio.create_task(callback(data))

eventBus = EventBus()
