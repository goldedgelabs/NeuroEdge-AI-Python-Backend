# backend-python/agents/WorkerAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class WorkerAgent:
    name = "WorkerAgent"

    def __init__(self):
        # Subscribe to DB events for new tasks
        eventBus.subscribe("task:new", self.handle_new_task)
        eventBus.subscribe("task:update", self.handle_task_update)

    async def execute_task(self, task: dict) -> dict:
        """
        Executes a given task. Tasks should have type, payload, and id.
        """
        task_id = task.get("id")
        if not task_id:
            logger.warn("[WorkerAgent] Task missing ID")
            return {"success": False, "reason": "Missing task ID"}

        logger.log(f"[WorkerAgent] Executing task {task_id} of type {task.get('type')}")

        # Example: Task execution logic
        try:
            result = {"task_id": task_id, "status": "completed"}
            # Save result in DB
            await db.set("tasks", task_id, result, "edge")
            eventBus.publish("db:update", {
                "collection": "tasks",
                "key": task_id,
                "value": result,
                "source": self.name
            })
            logger.log(f"[WorkerAgent] Task {task_id} executed successfully")
            return result
        except Exception as e:
            logger.error(f"[WorkerAgent] Failed to execute task {task_id}: {e}")
            return {"task_id": task_id, "status": "failed", "error": str(e)}

    async def handle_new_task(self, event: dict):
        task = event.get("value")
        if task:
            await self.execute_task(task)

    async def handle_task_update(self, event: dict):
        task = event.get("value")
        if task:
            logger.log(f"[WorkerAgent] Task updated: {task.get('id')}")

    async def recover(self, error: Exception):
        logger.error(f"[WorkerAgent] Recovering from error: {error}")
