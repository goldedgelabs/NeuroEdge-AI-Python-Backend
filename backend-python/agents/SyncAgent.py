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

    async def sync_collections(self, collections: list):
        """
        Synchronize specified collections from edge to shared storage.
        """
        synced = {}
        for collection in collections:
            records = await db.get_all(collection, target="edge")
            if not records:
                logger.warn(f"[SyncAgent] No records to sync in collection: {collection}")
                continue

            for key, value in records.items():
                await db.set(collection, key, value, target="shared")
            synced[collection] = len(records)
            logger.log(f"[SyncAgent] Collection synced: {collection} ({len(records)} records)")

        return synced

    async def handle_db_update(self, event: dict):
        logger.log(f"[SyncAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[SyncAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[SyncAgent] Recovering from error: {error}")
