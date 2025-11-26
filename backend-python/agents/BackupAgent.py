# backend-python/agents/BackupAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class BackupAgent:
    name = "BackupAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def backup_collection(self, collection: str):
        """
        Back up all records from a given collection.
        """
        records = await db.get_all(collection, target="edge")
        if not records:
            logger.warn(f"[BackupAgent] No records to backup in collection: {collection}")
            return None

        backup_id = f"backup_{collection}_{int(time.time()*1000)}"
        await db.set("backups", backup_id, {"collection": collection, "records": records, "timestamp": time.time()}, target="edge")
        eventBus.publish("db:update", {"collection": "backups", "key": backup_id, "value": records, "source": self.name})

        logger.log(f"[BackupAgent] Backup created for collection: {collection}")
        return {"backup_id": backup_id, "count": len(records)}

    async def handle_db_update(self, event: dict):
        logger.log(f"[BackupAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[BackupAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[BackupAgent] Recovering from error: {error}")
