# backend-python/agents/CorrectionAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class CorrectionAgent:
    name = "CorrectionAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def correct_entry(self, collection: str, key: str, corrections: dict):
        """
        Apply corrections to a record in the database.
        """
        record = await db.get(collection, key, target="edge")
        if not record:
            logger.warn(f"[CorrectionAgent] Record not found: {collection}:{key}")
            return None

        # Apply corrections
        record.update(corrections)

        # Save updated record
        await db.set(collection, key, record, target="edge")
        eventBus.publish("db:update", {"collection": collection, "key": key, "value": record, "source": self.name})

        logger.log(f"[CorrectionAgent] Record corrected: {collection}:{key} → {corrections}")
        return record

    async def handle_db_update(self, event: dict):
        logger.log(f"[CorrectionAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[CorrectionAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[CorrectionAgent] Recovering from error: {error}")
