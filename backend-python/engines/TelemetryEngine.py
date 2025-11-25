# backend-python/engines/TelemetryEngine.py

from typing import Any, Dict
from backend_python.db.db_manager import db
from backend_python.core.event_bus import event_bus
from backend_python.utils.logger import logger

class TelemetryEngine:
    name = "TelemetryEngine"

    def __init__(self):
        self.metrics = {}

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect and store telemetry data from devices or applications.
        """
        metric_id = input_data.get("metric_id", "unknown_metric")
        metric_record = {
            "collection": "telemetry",
            "id": metric_id,
            "type": input_data.get("type", "generic"),
            "value": input_data.get("value", None),
            "timestamp": input_data.get("timestamp"),
            "source": self.name
        }

        # Save to DB (edge)
        await db.set(metric_record["collection"], metric_record["id"], metric_record, "edge")

        # Publish DB update event
        event_bus.publish("db:update", {
            "collection": metric_record["collection"],
            "key": metric_record["id"],
            "value": metric_record,
            "source": self.name
        })

        logger.log(f"[{self.name}] DB updated: {metric_record['collection']}:{metric_record['id']}")
        return metric_record

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] Recovery from error: {error}")
