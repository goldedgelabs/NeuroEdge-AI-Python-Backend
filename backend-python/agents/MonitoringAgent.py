# backend-python/agents/MonitoringAgent.py

from core.agent_base import AgentBase
from core.db_manager import db
from core.event_bus import event_bus
from utils.logger import logger

class MonitoringAgent(AgentBase):
    name = "MonitoringAgent"

    def __init__(self):
        super().__init__()

    async def monitor_service(self, service_name: str, status: str):
        """
        Records the status of a service and triggers DB events.
        """
        status_record = {
            "service": service_name,
            "status": status
        }

        # Save to DB
        await db.set("services", service_name, status_record, "edge")
        event_bus.publish("db:update", {
            "collection": "services",
            "key": service_name,
            "value": status_record,
            "source": self.name
        })

        logger.log(f"[{self.name}] Service monitored: {service_name} = {status}")
        return status_record

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] MonitoringAgent error: {error}")
