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

    # Example method: process new ARV record
    async def process_new_arv(self, data: dict):
        collection = "arv_records"
        record_id = data.get("id")
        if record_id:
            await db.set(collection, record_id, data, target="edge")
            eventBus.publish("db:update", {"collection": collection, "key": record_id, "value": data, "source": self.name})
            logger.log(f"[ARVAgent] New ARV record saved: {record_id}")
            return {"success": True, "id": record_id}
        return {"success": False, "error": "No ID in data"}

    async def handle_db_update(self, event: dict):
        # Handle updates from DB if relevant
        if event.get("collection") == "arv_records":
            logger.log(f"[ARVAgent] Received DB update: {event['key']}")

    async def handle_db_delete(self, event: dict):
        # Handle deletions from DB if relevant
        if event.get("collection") == "arv_records":
            logger.log(f"[ARVAgent] Received DB delete: {event['key']}")

    async def recover(self, error: Exception):
        logger.error(f"[ARVAgent] Recovering from error: {error}")
