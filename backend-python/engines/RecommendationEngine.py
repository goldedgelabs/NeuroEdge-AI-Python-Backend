from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class RecommendationEngine:
    name = "RecommendationEngine"

    def __init__(self):
        self.recommendations = {}

    async def add_recommendation(self, rec_id: str, rec_data: dict):
        """Add or update a recommendation."""
        self.recommendations[rec_id] = rec_data

        # Save to DB and emit update event
        await db.set("recommendations", rec_id, rec_data, storage="edge")
        eventBus.publish("db:update", {
            "collection": "recommendations",
            "key": rec_id,
            "value": rec_data,
            "source": self.name
        })
        log(f"[{self.name}] Recommendation added/updated: {rec_id}")
        return rec_data

    async def get_recommendation(self, criteria: dict):
        """Retrieve recommendations matching criteria."""
        results = [
            rec for rec in self.recommendations.values()
            if all(rec.get(k) == v for k, v in criteria.items())
        ]
        log(f"[{self.name}] Recommendations retrieved: {results}")
        return results

    async def remove_recommendation(self, rec_id: str):
        """Remove a recommendation."""
        await db.delete("recommendations", rec_id, storage="edge")
        eventBus.publish("db:delete", {
            "collection": "recommendations",
            "key": rec_id,
            "source": self.name
        })
        log(f"[{self.name}] Removed recommendation: {rec_id}")
        self.recommendations.pop(rec_id, None)

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
