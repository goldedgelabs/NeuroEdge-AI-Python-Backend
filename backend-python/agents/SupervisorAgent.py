# backend-python/agents/SupervisorAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class SupervisorAgent:
    name = "SupervisorAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def supervise_task(self, task_id: str, status: str) -> dict:
        """
        Supervise a given task, updating its status.
        """
        logger.log(f"[SupervisorAgent] Supervising task {task_id}, status={status}")

        result = {"task_id": task_id, "status": status}
        await db.set("tasks", task_id, result, "edge")
        eventBus.publish("db:update", {
            "collection": "tasks",
            "key": task_id,
            "value": result,
            "source": self.name
        })
        logger.log(f"[SupervisorAgent] Task {task_id} updated in DB")

        return result

    async def handle_db_update(self, event: dict):
        logger.log(f"[SupervisorAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[SupervisorAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[SupervisorAgent] Recovering from error: {error}")
