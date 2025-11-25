from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class HealthEngine:
    name = "HealthEngine"

    def __init__(self):
        self.records = {}

    async def add_patient_record(self, patient_id, record):
        self.records[patient_id] = record
        # Write to DB and emit event
        await db.set("health_records", patient_id, record, storage="edge")
        eventBus.publish("db:update", {
            "collection": "health_records",
            "key": patient_id,
            "value": record,
            "source": self.name
        })
        log(f"[{self.name}] Patient record added: {patient_id}")
        return {"success": True, "patient_id": patient_id}

    async def update_patient_record(self, patient_id, record):
        if patient_id in self.records:
            self.records[patient_id].update(record)
            await db.set("health_records", patient_id, self.records[patient_id], storage="edge")
            eventBus.publish("db:update", {
                "collection": "health_records",
                "key": patient_id,
                "value": self.records[patient_id],
                "source": self.name
            })
            log(f"[{self.name}] Patient record updated: {patient_id}")
            return {"success": True}
        return {"success": False, "message": "Patient record not found"}

    async def remove_patient_record(self, patient_id):
        if patient_id in self.records:
            del self.records[patient_id]
            await db.delete("health_records", patient_id)
            eventBus.publish("db:delete", {
                "collection": "health_records",
                "key": patient_id,
                "source": self.name
            })
            log(f"[{self.name}] Patient record removed: {patient_id}")
            return {"success": True}
        return {"success": False, "message": "Patient record not found"}

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
