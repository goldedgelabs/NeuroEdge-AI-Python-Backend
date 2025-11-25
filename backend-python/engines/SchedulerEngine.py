# backend-python/engines/SchedulerEngine.py

from typing import Any, Dict
from backend_python.db.db_manager import db
from backend_python.core.event_bus import event_bus
from backend_python.utils.logger import logger
import asyncio
import datetime

class SchedulerEngine:
    name = "SchedulerEngine"

    def __init__(self):
        self.scheduled_tasks = []

    async def schedule_task(self, task_name: str, run_at: datetime.datetime, payload: Dict[str, Any]):
        """
        Schedule a task to be executed at a specific time.
        """
        task_record = {
            "collection": "scheduled_tasks",
            "id": f"{task_name}_{int(run_at.timestamp())}",
            "task_name": task_name,
            "run_at": run_at.isoformat(),
            "payload": payload,
            "status": "pending",
            "source": self.name
        }

        await db.set(task_record["collection"], task_record["id"], task_record, "edge")
        event_bus.publish("db:update", {
            "collection": task_record["collection"],
            "key": task_record["id"],
            "value": task_record,
            "source": self.name
        })
        logger.log(f"[{self.name}] Task scheduled: {task_record['id']}")
        self.scheduled_tasks.append(task_record)

    async def run(self, input_data: Dict[str, Any] = None):
        """
        Check for tasks that should run now and execute them.
        """
        now = datetime.datetime.utcnow()
        tasks_to_run = [t for t in self.scheduled_tasks if datetime.datetime.fromisoformat(t["run_at"]) <= now and t["status"] == "pending"]

        for task in tasks_to_run:
            logger.log(f"[{self.name}] Executing task: {task['id']}")
            task["status"] = "completed"
            await db.set(task["collection"], task["id"], task, "edge")
            event_bus.publish("db:update", {
                "collection": task["collection"],
                "key": task["id"],
                "value": task,
                "source": self.name
            })

        return {"executed": len(tasks_to_run)}

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] Recovery from error: {error}")
