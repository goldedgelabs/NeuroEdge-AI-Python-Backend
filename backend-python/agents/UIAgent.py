from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class UIAgent:
    name = "UIAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def update_ui_component(self, component_id: str, data: dict):
        """
        Update a UI component's state in the database.
        """
        if not component_id or not data:
            logger.warn(f"[UIAgent] Missing component_id or data")
            return None

        record = await db.get("ui_components", component_id, target="edge") or {}
        record.update(data)

        await db.set("ui_components", component_id, record, target="edge")
        eventBus.publish("db:update", {"collection": "ui_components", "key": component_id, "value": record, "source": self.name})

        logger.log(f"[UIAgent] Component updated: {component_id} → {data}")
        return record

    async def handle_db_update(self, event: dict):
        logger.log(f"[UIAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[UIAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[UIAgent] Recovering from error: {error}")
