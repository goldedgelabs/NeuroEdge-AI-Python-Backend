# backend-python/agents/SummarizationAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class SummarizationAgent:
    name = "SummarizationAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def summarize_text(self, text: str, max_length: int = 150) -> dict:
        """
        Summarize the input text.
        """
        logger.log(f"[SummarizationAgent] Summarizing text of length {len(text)}")

        # Simple summarization (for example purposes)
        summary = text[:max_length] + ("..." if len(text) > max_length else "")

        # Save summary to DB
        key = f"summary_{hash(text)}"
        result = {"text": text, "summary": summary}
        await db.set("summaries", key, result, "edge")
        eventBus.publish("db:update", {
            "collection": "summaries",
            "key": key,
            "value": result,
            "source": self.name
        })
        logger.log(f"[SummarizationAgent] Summary saved to DB with key: {key}")

        return result

    async def handle_db_update(self, event: dict):
        logger.log(f"[SummarizationAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[SummarizationAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[SummarizationAgent] Recovering from error: {error}")
