# backend-python/agents/DataProcessingAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import asyncio

class DataProcessingAgent:
    name = "DataProcessingAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def process_record(self, collection: str, record_id: str):
        """
        Fetches a record from the DB, processes it, and updates it.
        """
        record = await db.get(collection, record_id)
        if not record:
            logger.warn(f"[DataProcessingAgent] Record not found: {collection}:{record_id}")
            return {"error": "record_not_found"}

        # Example processing: add a processed flag
        record["processed"] = True
        await db.set(collection, record_id, record, target="edge")
        eventBus.publish("db:update", {"collection": collection, "key": record_id, "value": record, "source": self.name})
        logger.log(f"[DataProcessingAgent] Record processed: {collection}:{record_id}")
        return record

    async def batch_process(self, collection: str, record_ids: list):
        """
        Processes multiple records in batch.
        """
        results = []
        for rid in record_ids:
            result = await self.process_record(collection, rid)
            results.append(result)
        return results

    async def handle_db_update(self, event: dict):
        logger.log(f"[DataProcessingAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[DataProcessingAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[DataProcessingAgent] Recovering from error: {error}")
