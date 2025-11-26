from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class RealTimeRecommenderEngine:
    name = "RealTimeRecommenderEngine"

    def __init__(self):
        self.recommendations = {}

    async def add_item(self, item_id: str, metadata: dict):
        """Add or update an item for recommendation."""
        self.recommendations[item_id] = metadata

        # Save to DB and emit update event
        await db.set("recommendation_items", item_id, metadata, storage="edge")
        eventBus.publish("db:update", {
            "collection": "recommendation_items",
            "key": item_id,
            "value": metadata,
            "source": self.name
        })
        log(f"[{self.name}] Item added/updated: {item_id}")
        return metadata

    async def recommend(self, user_id: str, top_n: int = 5):
        """Generate simple real-time recommendations (top N recent items)."""
        if not self.recommendations:
            return {"error": "No items available"}
        
        sorted_items = list(self.recommendations.items())[-top_n:]
        recommendation_list = [{ "item_id": k, "metadata": v } for k, v in sorted_items]

        log(f"[{self.name}] Recommendations for user {user_id}: {recommendation_list}")
        return recommendation_list

    async def remove_item(self, item_id: str):
        """Remove an item from recommendations."""
        await db.delete("recommendation_items", item_id, storage="edge")
        eventBus.publish("db:delete", {
            "collection": "recommendation_items",
            "key": item_id,
            "source": self.name
        })
        log(f"[{self.name}] Removed item: {item_id}")
        self.recommendations.pop(item_id, None)

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
