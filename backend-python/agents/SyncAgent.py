# backend-python/agents/SyncAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class SyncAgent:
    name = "SyncAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def sync_collections(self, source_collection: str, target_collection: str) -> dict:
        """
        Synchronize data from source collection to target collection.
        """
        records = await db.get_all(source_collection, target="edge")
        if not records:
            logger.warn(f"[SyncAgent] No records to sync from: {source_collection}")
            return {"error": "No records to sync"}

        for key, record in records.items():
            await db.set(target_collection, key, record, target="edge")
            eventBus.publish("db:update", {
                "collection": target_collection,
                "key": key,
                "value": record,
                "source": self.name
            })

        logger.log(f"[SyncAgent] Synced {len(records)} records from {source_collection} to {target_collection}")
        return {"synced_count": len(records), "target_collection": target_collection}

    async def handle_db_update(self, event: dict):
        logger.log(f"[SyncAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[SyncAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[SyncAgent] Recovering from error: {error}")
