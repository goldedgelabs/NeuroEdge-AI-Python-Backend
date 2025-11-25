# backend-python/agents/AnalyticsAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class AnalyticsAgent:
    name = "AnalyticsAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def analyze_data(self, collection: str, data: dict):
        record_id = data.get("id")
        if not record_id:
            return {"success": False, "error": "No ID provided"}
        
        # Simulate analysis
        analysis_result = {"summary": f"Analyzed {collection} record {record_id}"}
        # Save analysis result to DB
        await db.set("analytics", record_id, analysis_result, target="edge")
        eventBus.publish("db:update", {"collection": "analytics", "key": record_id, "value": analysis_result, "source": self.name})
        logger.log(f"[AnalyticsAgent] Analysis saved for record: {record_id}")
        return {"success": True, "id": record_id, "analysis": analysis_result}

    async def handle_db_update(self, event: dict):
        # React to relevant DB updates
        logger.log(f"[AnalyticsAgent] Received DB update: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        # React to relevant DB deletes
        logger.log(f"[AnalyticsAgent] Received DB delete: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[AnalyticsAgent] Recovering from error: {error}")
