# backend-python/agents/PersonalAgent.py

from core.agent_base import AgentBase
from core.db_manager import db
from core.event_bus import event_bus
from utils.logger import logger

class PersonalAgent(AgentBase):
    name = "PersonalAgent"

    def __init__(self):
        super().__init__()
        self.profile = {}

    async def update_profile(self, user_id: str, data: dict):
        """
        Update user profile information and store in DB.
        """
        self.profile[user_id] = data
        await db.set("personal_profiles", user_id, data, "edge")
        event_bus.publish("db:update", {"collection": "personal_profiles", "key": user_id, "value": data, "source": self.name})
        logger.log(f"[{self.name}] Profile updated for user {user_id}")
        return {"success": True, "user_id": user_id}

    async def get_profile(self, user_id: str):
        """
        Retrieve a user profile from DB or local cache.
        """
        profile = self.profile.get(user_id)
        if not profile:
            profile = await db.get("personal_profiles", user_id)
        return profile

    async def handleDBUpdate(self, data):
        """
        Respond to DB updates for personal data.
        """
        if data.get("collection") == "personal_profiles":
            key = data.get("key")
            value = data.get("value")
            self.profile[key] = value
            logger.log(f"[{self.name}] Updated local cache for {key}")

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] PersonalAgent error: {error}")
