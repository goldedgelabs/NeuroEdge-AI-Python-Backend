from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class PhoneSecurityEngine:
    name = "PhoneSecurityEngine"

    def __init__(self):
        self.devices = {}

    async def register_device(self, device_id: str, info: dict):
        """Register a new device or update existing."""
        self.devices[device_id] = info

        # Save to DB and emit update event
        await db.set("devices", device_id, info, storage="edge")
        eventBus.publish("db:update", {
            "collection": "devices",
            "key": device_id,
            "value": info,
            "source": self.name
        })
        log(f"[{self.name}] Registered/Updated device: {device_id}")
        return info

    async def check_security(self, device_id: str):
        """Perform security checks for a device."""
        device = self.devices.get(device_id)
        if not device:
            return {"error": "Device not found"}

        # Example check
        status = "secure" if device.get("status") == "active" else "alert"
        log(f"[{self.name}] Device {device_id} security status: {status}")
        return {"device_id": device_id, "status": status}

    async def remove_device(self, device_id: str):
        """Remove device from system."""
        await db.delete("devices", device_id, storage="edge")
        eventBus.publish("db:delete", {
            "collection": "devices",
            "key": device_id,
            "source": self.name
        })
        log(f"[{self.name}] Removed device: {device_id}")
        self.devices.pop(device_id, None)

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
