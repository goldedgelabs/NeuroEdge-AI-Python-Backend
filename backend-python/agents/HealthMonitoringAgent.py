# backend-python/agents/HealthMonitoringAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class HealthMonitoringAgent:
    name = "HealthMonitoringAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def monitor_system(self, metrics: dict) -> dict:
        """
        Monitor system health metrics and log critical alerts.
        """
        if not metrics:
            logger.warn(f"[HealthMonitoringAgent] No metrics provided")
            return {"error": "No metrics provided"}

        alerts = []
        if metrics.get("cpu") and metrics["cpu"] > 85:
            alerts.append("High CPU usage detected")
        if metrics.get("memory") and metrics["memory"] > 90:
            alerts.append("High memory usage detected")
        if metrics.get("disk") and metrics["disk"] > 90:
            alerts.append("High disk usage detected")

        record = {
            "timestamp": time.time(),
            "metrics": metrics,
            "alerts": alerts
        }

        record_id = f"health_{int(time.time()*1000)}"
        await db.set("system_health_logs", record_id, record, target="edge")
        eventBus.publish("db:update", {
            "collection": "system_health_logs",
            "key": record_id,
            "value": record,
            "source": self.name
        })

        logger.log(f"[HealthMonitoringAgent] System health logged with {len(alerts)} alerts")
        return {"record_id": record_id, "alerts": alerts}

    async def handle_db_update(self, event: dict):
        logger.log(f"[HealthMonitoringAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[HealthMonitoringAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[HealthMonitoringAgent] Recovering from error: {error}")
