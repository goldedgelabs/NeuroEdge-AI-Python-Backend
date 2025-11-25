# backend-python/agents/CreativityAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class CreativityAgent:
    name = "CreativityAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def generate_content(self, prompt: str, user_id: str):
        """
        Generate creative content based on a prompt.
        For now, it will return a simple formatted string.
        """
        content = f"Creative output for '{prompt}'"

        # Store generated content in DB
        key = f"{user_id}-{hash(prompt)}"
        content_record = {
            "user_id": user_id,
            "prompt": prompt,
            "content": content
        }
        await db.set("creative_content", key, content_record, target="edge")
        eventBus.publish("db:update", {"collection": "creative_content", "key": key, "value": content_record, "source": self.name})

        logger.log(f"[CreativityAgent] Creative content saved: {key}")
        return content

    async def handle_db_update(self, event: dict):
        logger.log(f"[CreativityAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[CreativityAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[CreativityAgent] Recovering from error: {error}")
