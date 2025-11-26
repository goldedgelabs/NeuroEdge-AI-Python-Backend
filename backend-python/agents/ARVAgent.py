# backend-python/agents/ARVAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class ARVAgent:
    name = "ARVAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)
        logger.log(f"[ARVAgent] Initialized")

    async def process_arv_data(self, collection: str, key: str, data: dict):
        """
        Process and store ARV data in the database.
        """
        record = {
            "id": key,
            "collection": collection,
            "payload": data
        }

        # Save record in edge DB
        await db.set(collection, key, record, target="edge")

        # Emit DB update event
        eventBus.publish("db:update", {"collection": collection, "key": key, "value": record, "source": self.name})
        logger.log(f"[ARVAgent] DB updated → {collection}:{key}")
        return record

    async def handle_db_update(self, event: dict):
        logger.log(f"[ARVAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[ARVAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[ARVAgent] Recovering from error: {error}")
