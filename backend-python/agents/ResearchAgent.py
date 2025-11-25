# backend-python/agents/ResearchAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class ResearchAgent:
    name = "ResearchAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def conduct_research(self, topic: str, data: dict) -> dict:
        """
        Conduct research on a given topic using provided data.
        """
        logger.log(f"[ResearchAgent] Conducting research on topic: {topic}")

        # Example research processing: collect summary statistics
        result = {k: {"count": len(v) if isinstance(v, list) else 1, "sample": v[:3] if isinstance(v, list) else v} for k, v in data.items()}

        # Save research results to DB
        if result:
            await db.set("research_results", f"research_{topic}", result, "edge")
            eventBus.publish("db:update", {
                "collection": "research_results",
                "key": f"research_{topic}",
                "value": result,
                "source": self.name
            })
            logger.log(f"[ResearchAgent] Research results saved to DB.")

        return result

    async def handle_db_update(self, event: dict):
        logger.log(f"[ResearchAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[ResearchAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[ResearchAgent] Recovering from error: {error}")
