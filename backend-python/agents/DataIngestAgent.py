# backend-python/agents/DataIngestAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import asyncio

class DataIngestAgent:
    name = "DataIngestAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def ingest_data(self, collection: str, data_id: str, data: dict):
        """
        Ingest data into a specific collection.
        """
        await db.set(collection, data_id, data, target="edge")
        eventBus.publish("db:update", {"collection": collection, "key": data_id, "value": data, "source": self.name})
        logger.log(f"[DataIngestAgent] Data ingested: {collection}:{data_id}")
        return {"status": "success", "collection": collection, "id": data_id}

    async def batch_ingest(self, collection: str, items: list):
        """
        Batch ingest multiple items.
        Each item must have an 'id' and 'data'.
        """
        results = []
        for item in items:
            result = await self.ingest_data(collection, item["id"], item["data"])
            results.append(result)
        return results

    async def handle_db_update(self, event: dict):
        logger.log(f"[DataIngestAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[DataIngestAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[DataIngestAgent] Recovering from error: {error}")
