from utils.event_bus import event_bus
from db_manager import db_manager
from replication_manager import replication_manager

def initialize_db_wiring():
    """Subscribe global event bus to DB replication."""
    async def on_db_update(data):
        # When any engine/agent updates DB, replicate edge → shared
        collection = data.get("collection")
        await replication_manager.replicate_edge_to_shared(collection)

    event_bus.subscribe("db:update", lambda data: on_db_update(data))
    event_bus.subscribe("db:delete", lambda data: on_db_update(data))
