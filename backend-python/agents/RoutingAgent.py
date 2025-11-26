# backend-python/agents/RoutingAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class RoutingAgent:
    name = "RoutingAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def route_request(self, collection: str, request: dict) -> dict:
        """
        Determine routing for incoming requests.
        """
        # Example routing logic: choose node based on hash of user ID
        user_id = request.get("user_id", "unknown")
        node = f"node_{hash(user_id) % 5}"

        result = {
            "timestamp": time.time(),
            "user_id": user_id,
            "assigned_node": node,
            "request": request
        }

        # Save routing info to DB
        record_id = f"route_{int(time.time()*1000)}"
        await db.set(collection, record_id, result, target="edge")
        eventBus.publish("db:update", {
            "collection": collection,
            "key": record_id,
            "value": result,
            "source": self.name
        })

        logger.log(f"[RoutingAgent] Routing info saved: {collection}:{record_id}")
        return result

    async def handle_db_update(self, event: dict):
        logger.log(f"[RoutingAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[RoutingAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[RoutingAgent] Recovering from error: {error}")
