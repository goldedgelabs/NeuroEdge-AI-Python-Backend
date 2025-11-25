# backend-python/agents/DiscoveryAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import asyncio

class DiscoveryAgent:
    name = "DiscoveryAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def discover_resources(self, query: dict):
        """
        Discover new resources, datasets, or devices based on a query.
        """
        try:
            collection = query.get("collection", "resources")
            filters = query.get("filters", {})

            # Fetch all records in the collection
            records = await db.get_all(collection)

            # Apply filters
            discovered = [r for r in records if all(r.get(k) == v for k, v in filters.items())]

            logger.log(f"[DiscoveryAgent] Discovered {len(discovered)} items in collection {collection}")

            return {"collection": collection, "discovered": discovered}

        except Exception as e:
            await self.recover(e)
            return {"error": "discovery_failed"}

    async def handle_db_update(self, event: dict):
        logger.log(f"[DiscoveryAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[DiscoveryAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[DiscoveryAgent] Recovering from error: {error}")
