# backend-python/agents/BackupAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time
import copy

class BackupAgent:
    name = "BackupAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def create_backup(self, collection: str) -> dict:
        """
        Create a backup of all records in a given collection.
        """
        records = await db.get_all(collection, target="edge")
        if records is None:
            logger.warn(f"[BackupAgent] No records found for backup: {collection}")
            return {"error": "No records to backup"}

        backup_data = copy.deepcopy(records)
        backup_id = f"backup_{collection}_{int(time.time()*1000)}"
        await db.set("backups", backup_id, {"collection": collection, "data": backup_data, "timestamp": time.time()}, target="edge")

        eventBus.publish("db:update", {
            "collection": "backups",
            "key": backup_id,
            "value": {"collection": collection, "data": backup_data},
            "source": self.name
        })

        logger.log(f"[BackupAgent] Backup created: backups:{backup_id}")
        return {"backup_id": backup_id, "records_count": len(backup_data)}

    async def restore_backup(self, backup_id: str) -> dict:
        """
        Restore a backup by its ID.
        """
        backup = await db.get("backups", backup_id, target="edge")
        if not backup:
            logger.warn(f"[BackupAgent] Backup not found: {backup_id}")
            return {"error": "Backup not found"}

        collection = backup["collection"]
        for key, record in backup["data"].items():
            await db.set(collection, key, record, target="edge")

        logger.log(f"[BackupAgent] Backup restored: {backup_id}")
        return {"restored_collection": collection, "records_restored": len(backup["data"])}

    async def handle_db_update(self, event: dict):
        logger.log(f"[BackupAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[BackupAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[BackupAgent] Recovering from error: {error}")
