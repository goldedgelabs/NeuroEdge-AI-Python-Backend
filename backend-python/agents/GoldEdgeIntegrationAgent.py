# backend-python/agents/GoldEdgeIntegrationAgent.py

from core.agent_base import AgentBase
from core.db_manager import db
from core.event_bus import event_bus
from utils.logger import logger

class GoldEdgeIntegrationAgent(AgentBase):
    name = "GoldEdgeIntegrationAgent"

    def __init__(self):
        super().__init__()

    async def integrate_gold_edge(self, data: dict):
        """
        Handles integration between GoldEdge systems and local NeuroEdge databases.
        """
        record = {
            "id": data.get("id"),
            "collection": "gold_edge_data",
            "data": data
        }

        # Write to DB
        await db.set(record["collection"], record["id"], record, "edge")

        # Publish DB update event
        event_bus.publish("db:update", {
            "collection": record["collection"],
            "key": record["id"],
            "value": record,
            "source": self.name
        })

        logger.log(f"[{self.name}] GoldEdge integration completed: {record['id']}")
        return record

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] Error in GoldEdgeIntegrationAgent: {error}")
