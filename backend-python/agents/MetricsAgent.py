# backend-python/agents/MetricsAgent.py

from core.agent_base import AgentBase
from core.db_manager import db
from core.event_bus import event_bus
from utils.logger import logger

class MetricsAgent(AgentBase):
    name = "MetricsAgent"

    def __init__(self):
        super().__init__()

    async def record_metric(self, metric_name: str, value: float):
        """
        Records a single metric to the DB and emits a db:update event.
        """
        metric_data = {
            "name": metric_name,
            "value": value
        }

        # Save to DB
        await db.set("metrics", metric_name, metric_data, "edge")
        event_bus.publish("db:update", {
            "collection": "metrics",
            "key": metric_name,
            "value": metric_data,
            "source": self.name
        })

        logger.log(f"[{self.name}] Metric recorded: {metric_name} = {value}")
        return metric_data

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] MetricsAgent error: {error}")
