from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class RecoveryAgent:
    name = "RecoveryAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def recover_system(self, error_info: dict):
        """
        Handles system recovery from faults or failures.
        """
        if not error_info:
            logger.warn(f"[RecoveryAgent] Missing error information")
            return None

        recovery_record = {
            "timestamp": time.time(),
            "error_info": error_info,
            "status": "recovery_initiated"
        }

        record_id = f"recovery_{int(time.time()*1000)}"
        await db.set("recovery_logs", record_id, recovery_record, target="edge")
        eventBus.publish("db:update", {"collection": "recovery_logs", "key": record_id, "value": recovery_record, "source": self.name})

        logger.log(f"[RecoveryAgent] Recovery initiated: {record_id}")
        return {"id": record_id, "recovery": recovery_record}

    async def handle_db_update(self, event: dict):
        logger.log(f"[RecoveryAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[RecoveryAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[RecoveryAgent] Recovering from error: {error}")
