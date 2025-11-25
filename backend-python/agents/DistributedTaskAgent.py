# backend-python/agents/DistributedTaskAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import asyncio
import uuid

class DistributedTaskAgent:
    name = "DistributedTaskAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)
        self.task_queue = asyncio.Queue()

    async def add_task(self, task: dict):
        """
        Add a new task to the distributed queue.
        """
        try:
            task_id = task.get("id") or str(uuid.uuid4())
            task["id"] = task_id

            await self.task_queue.put(task)
            logger.log(f"[DistributedTaskAgent] Task added: {task_id}")

            # Persist task to DB
            await db.set("tasks", task_id, task, "edge")
            eventBus.publish("db:update", {"collection": "tasks", "key": task_id, "value": task, "source": self.name})

            return {"success": True, "task_id": task_id}

        except Exception as e:
            await self.recover(e)
            return {"error": "task_add_failed"}

    async def execute_task(self):
        """
        Execute tasks from the queue sequentially.
        """
        while True:
            task = await self.task_queue.get()
            try:
                task_name = task.get("name", "UnnamedTask")
                logger.log(f"[DistributedTaskAgent] Executing task {task['id']}: {task_name}")

                # Placeholder: implement actual distributed execution logic
                await asyncio.sleep(task.get("duration", 1))

                logger.log(f"[DistributedTaskAgent] Completed task {task['id']}")
            except Exception as e:
                await self.recover(e)
            finally:
                self.task_queue.task_done()

    async def handle_db_update(self, event: dict):
        logger.log(f"[DistributedTaskAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[DistributedTaskAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[DistributedTaskAgent] Recovering from error: {error}")
