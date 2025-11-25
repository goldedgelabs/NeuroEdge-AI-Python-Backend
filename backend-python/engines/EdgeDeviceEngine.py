# EdgeDeviceEngine.py
from core.dbManager import db
from core.eventBus import eventBus

class EdgeDeviceEngine:
    name = "EdgeDeviceEngine"

    async def run(self, input_data):
        # Process input_data for edge devices
        result = {"collection": "edge_devices", "id": input_data.get("id"), **input_data}
        await db.set("edge_devices", result["id"], result, layer="edge")
        eventBus.publish("db:update", {"collection": "edge_devices", "key": result["id"], "value": result, "source": self.name})
        return result

    async def recover(self, error):
        print(f"[EdgeDeviceEngine] Recovered from error: {error}")
        return {"error": "Recovered from failure"}
