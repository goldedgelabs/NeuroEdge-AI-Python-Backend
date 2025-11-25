# backend-python/agents/GPIAgent.py

from core.agent_base import AgentBase
from core.db_manager import db
from core.event_bus import event_bus
from utils.logger import logger

class GPIAgent(AgentBase):
    name = "GPIAgent"

    def __init__(self):
        super().__init__()

    async def update_gpi_metrics(self, metrics: dict):
        """
        Updates Global Performance Index metrics in the database.
        """
        record = {
            "id": metrics.get("id"),
            "collection": "gpi_metrics",
            "data": metrics
        }

        # Store in DB
        await db.set(record["collection"], record["id"], record, "edge")

        # Trigger DB update event
        event_bus.publish("db:update", {
            "collection": record["collection"],
            "key": record["id"],
            "value": record,
            "source": self.name
        })

        logger.log(f"[{self.name}] GPI metrics updated: {record['id']}")
        return record

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] Error occurred: {error}")
