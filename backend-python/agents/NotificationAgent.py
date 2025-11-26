# backend-python/agents/NotificationAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class NotificationAgent:
    name = "NotificationAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def send_notification(self, user_id: str, message: str, metadata: dict = None) -> dict:
        """
        Send a notification to a user and save it in the DB.
        """
        notification = {
            "user_id": user_id,
            "message": message,
            "metadata": metadata or {},
            "timestamp": time.time(),
            "status": "sent"
        }

        record_id = f"notif_{int(time.time()*1000)}"
        await db.set("notifications", record_id, notification, target="edge")
        eventBus.publish("db:update", {
            "collection": "notifications",
            "key": record_id,
            "value": notification,
            "source": self.name
        })

        logger.log(f"[NotificationAgent] Notification sent: notifications:{record_id}")
        return {"id": record_id, "notification": notification}

    async def handle_db_update(self, event: dict):
        logger.log(f"[NotificationAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[NotificationAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[NotificationAgent] Recovering from error: {error}")
