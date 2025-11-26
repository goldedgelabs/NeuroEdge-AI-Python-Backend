# backend-python/core/eventBus.py
import asyncio
from collections import defaultdict
from utils.logger import logger

class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type: str, callback):
        self.subscribers[event_type].append(callback)
        logger.log(f"[EventBus] Subscribed to event: {event_type}")

    def publish(self, event_type: str, data: dict):
        logger.log(f"[EventBus] Publishing event: {event_type} → {data.get('collection', '')}:{data.get('key', '')}")
        for callback in self.subscribers[event_type]:
            # Call asynchronously if coroutine
            if asyncio.iscoroutinefunction(callback):
                asyncio.create_task(callback(data))
            else:
                callback(data)

eventBus = EventBus()
