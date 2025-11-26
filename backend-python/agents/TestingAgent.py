from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class TestingAgent:
    name = "TestingAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def run_test(self, test_name: str, data: dict):
        """
        Execute a test scenario and store results.
        """
        if not test_name or not data:
            logger.warn(f"[TestingAgent] Missing test_name or data")
            return None

        result = {
            "timestamp": time.time(),
            "test_name": test_name,
            "data": data,
            "status": "pending"
        }

        record_id = f"test_{int(time.time()*1000)}"
        await db.set("test_results", record_id, result, target="edge")
        eventBus.publish("db:update", {"collection": "test_results", "key": record_id, "value": result, "source": self.name})

        logger.log(f"[TestingAgent] Test recorded: {record_id} → {test_name}")
        return {"id": record_id, "result": result}

    async def handle_db_update(self, event: dict):
        logger.log(f"[TestingAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[TestingAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[TestingAgent] Recovering from error: {error}")
