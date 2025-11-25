# backend-python/agents/CollaborationAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class CollaborationAgent:
    name = "CollaborationAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def create_collaboration(self, project_id: str, users: list):
        """
        Create a new collaboration project with assigned users.
        """
        collab_record = {
            "project_id": project_id,
            "users": users,
            "status": "active"
        }

        # Store in DB
        await db.set("collaborations", project_id, collab_record, target="edge")
        eventBus.publish("db:update", {"collection": "collaborations", "key": project_id, "value": collab_record, "source": self.name})

        logger.log(f"[CollaborationAgent] Collaboration created: {project_id} with users {users}")
        return collab_record

    async def handle_db_update(self, event: dict):
        logger.log(f"[CollaborationAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[CollaborationAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[CollaborationAgent] Recovering from error: {error}")
