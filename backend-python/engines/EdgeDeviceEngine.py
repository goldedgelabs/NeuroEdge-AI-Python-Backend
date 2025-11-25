from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class EdgeDeviceEngine:
    name = "EdgeDeviceEngine"

    def __init__(self):
        self.devices = {}

    async def register_device(self, device_id, metadata):
        self.devices[device_id] = metadata
        # Write to DB and emit event
        await db.set("devices", device_id, metadata, storage="edge")
        eventBus.publish("db:update", {
            "collection": "devices",
            "key": device_id,
            "value": metadata,
            "source": self.name
        })
        log(f"[{self.name}] Device registered: {device_id}")
        return {"success": True, "device_id": device_id}

    async def remove_device(self, device_id):
        if device_id in self.devices:
            del self.devices[device_id]
            await db.delete("devices", device_id)
            eventBus.publish("db:delete", {"collection": "devices", "key": device_id, "source": self.name})
            log(f"[{self.name}] Device removed: {device_id}")
            return {"success": True}
        return {"success": False, "message": "Device not found"}

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
