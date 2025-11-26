# backend-python/db/replicationManager.py
from core.dbManager import db
from core.eventBus import eventBus
from utils.logger import logger

async def replicateEdgeToShared():
    """
    Replicate all edge DB collections to shared DB
    """
    logger.log("[ReplicationManager] Starting edge → shared replication...")
    for collection, items in db.store.get("edge", {}).items():
        for key, value in items.items():
            await db.set(collection, key, value, target="shared")
            eventBus.publish("db:update", {"collection": collection, "key": key, "value": value, "source": "replicationManager"})
    logger.log("[ReplicationManager] Edge → shared replication complete.")

# Subscribe to edge updates for live replication
async def on_edge_update(event):
    await db.set(event["collection"], event["key"], event["value"], target="shared")

eventBus.subscribe("db:update", on_edge_update)
