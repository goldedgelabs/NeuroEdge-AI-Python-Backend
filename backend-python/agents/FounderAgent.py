# backend-python/agents/FounderAgent.py

from core.agent_base import AgentBase
from core.db_manager import db
from core.event_bus import event_bus
from utils.logger import logger

class FounderAgent(AgentBase):
    name = "FounderAgent"

    def __init__(self):
        super().__init__()

    async def register_founder(self, founder_info: dict):
        """
        Registers a founder profile in the system.
        """
        record = {
            "id": founder_info.get("id"),
            "collection": "founders",
            "data": founder_info
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

        logger.log(f"[{self.name}] Founder registered: {record['id']}")
        return record

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] Error occurred: {error}")
