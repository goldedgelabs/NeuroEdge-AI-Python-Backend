# CriticEngine.py
from core.dbManager import db
from core.eventBus import eventBus

class CriticEngine:
    name = "CriticEngine"

    async def run(self, input_data):
        # Analyze and critique input
        result = {"collection": "critic", "id": input_data.get("id"), "feedback": input_data.get("text"), **input_data}
        await db.set("critic", result["id"], result, layer="edge")
        eventBus.publish("db:update", {"collection": "critic", "key": result["id"], "value": result, "source": self.name})
        return result

    async def recover(self, error):
        print(f"[CriticEngine] Recovered from error: {error}")
        return {"error": "Recovered from failure"}
