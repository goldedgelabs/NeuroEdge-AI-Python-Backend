# backend-python/agents/DeviceProtectionAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import asyncio

class DeviceProtectionAgent:
    name = "DeviceProtectionAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def protect_device(self, device_info: dict):
        """
        Apply protection policies or alerts for devices.
        """
        try:
            device_id = device_info.get("id")
            if not device_id:
                return {"error": "device_id_missing"}

            # Example protection logic: block device if flagged
            status = "safe"
            if device_info.get("threat_level", 0) > 5:
                status = "blocked"

            result = {
                "device_id": device_id,
                "status": status,
                "info": device_info
            }

            # Save protection status to DB
            await db.set("devices", device_id, result, target="edge")
            eventBus.publish("db:update", {
                "collection": "devices",
                "key": device_id,
                "value": result,
                "source": self.name
            })

            logger.log(f"[DeviceProtectionAgent] Device {device_id} status: {status}")
            return result
        except Exception as e:
            await self.recover(e)
            return {"error": "protection_failed"}

    async def handle_db_update(self, event: dict):
        logger.log(f"[DeviceProtectionAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[DeviceProtectionAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[DeviceProtectionAgent] Recovering from error: {error}")
