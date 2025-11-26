# backend-python/agents/LoadBalancingAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class LoadBalancingAgent:
    name = "LoadBalancingAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def distribute_tasks(self, tasks: list, nodes: list) -> dict:
        """
        Distribute tasks evenly across available nodes.
        """
        if not tasks or not nodes:
            logger.warn(f"[LoadBalancingAgent] No tasks or nodes provided")
            return {"error": "Tasks or nodes missing"}

        distribution = {node: [] for node in nodes}
        for i, task in enumerate(tasks):
            node = nodes[i % len(nodes)]
            distribution[node].append(task)

        # Optionally store distribution in DB
        record_id = f"load_{int(time.time()*1000)}"
        await db.set("task_distribution", record_id, distribution, target="edge")
        eventBus.publish("db:update", {
            "collection": "task_distribution",
            "key": record_id,
            "value": distribution,
            "source": self.name
        })

        logger.log(f"[LoadBalancingAgent] Distributed {len(tasks)} tasks across {len(nodes)} nodes")
        return {"distribution_id": record_id, "distribution": distribution}

    async def handle_db_update(self, event: dict):
        logger.log(f"[LoadBalancingAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[LoadBalancingAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[LoadBalancingAgent] Recovering from error: {error}")
