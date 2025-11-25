# backend-python/agents/ResearchAnalyticsAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class ResearchAnalyticsAgent:
    name = "ResearchAnalyticsAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def analyze(self, dataset: dict) -> dict:
        """
        Analyze a given dataset and return analytics results.
        """
        logger.log(f"[ResearchAnalyticsAgent] Analyzing dataset with {len(dataset)} records.")
        # Example analytics: count numeric values per key
        result = {k: sum(v for v in dataset[k] if isinstance(v, (int, float))) for k in dataset}
        
        # Save result to DB
        if result:
            await db.set("research_analytics", f"analysis_{self.name}", result, "edge")
            eventBus.publish("db:update", {
                "collection": "research_analytics",
                "key": f"analysis_{self.name}",
                "value": result,
                "source": self.name
            })
            logger.log(f"[ResearchAnalyticsAgent] Analytics results saved to DB.")
        
        return result

    async def handle_db_update(self, event: dict):
        logger.log(f"[ResearchAnalyticsAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[ResearchAnalyticsAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[ResearchAnalyticsAgent] Recovering from error: {error}")
