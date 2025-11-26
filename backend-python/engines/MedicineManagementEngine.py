from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus


class MedicineManagementEngine:
    name = "MedicineManagementEngine"

    def __init__(self):
        self.records = {}

    async def add_medicine(self, medicine_id: str, details: dict):
        """Add a new medicine record."""
        record = {
            "id": medicine_id,
            "details": details
        }

        await db.set("medicines", medicine_id, record, storage="edge")

        eventBus.publish("db:update", {
            "collection": "medicines",
            "key": medicine_id,
            "value": record,
            "source": self.name
        })

        log(f"[{self.name}] Added medicine: {medicine_id}")
        return record

    async def update_medicine(self, medicine_id: str, patch: dict):
        """Update existing medicine record."""
        existing = await db.get("medicines", medicine_id, storage="edge") or {}

        updated = {**existing, **patch, "id": medicine_id}
        await db.set("medicines", medicine_id, updated, storage="edge")

        eventBus.publish("db:update", {
            "collection": "medicines",
            "key": medicine_id,
            "value": updated,
            "source": self.name
        })

        log(f"[{self.name}] Updated medicine: {medicine_id}")
        return updated

    async def remove_medicine(self, medicine_id: str):
        """Remove a medicine record."""
        await db.delete("medicines", medicine_id)

        eventBus.publish("db:delete", {
            "collection": "medicines",
            "key": medicine_id,
            "source": self.name
        })

        log(f"[{self.name}] Removed medicine: {medicine_id}")
        return {"success": True, "id": medicine_id}

    async def list_medicines(self):
        """Return all medicines."""
        records = await db.all("medicines", storage="edge")
        return records

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
