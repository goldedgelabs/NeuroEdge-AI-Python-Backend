from typing import Dict, Any
from utils.logger import log, warn
from utils.helpers import generate_id

class DBManager:
    def __init__(self):
        # Edge storage: in-memory dictionary
        self.edge_store: Dict[str, Dict[str, Any]] = {}
        # Shared storage (can be remote or another dict)
        self.shared_store: Dict[str, Dict[str, Any]] = {}

    async def set(self, collection: str, key: str, value: Dict[str, Any], storage: str = "edge"):
        store = self.edge_store if storage == "edge" else self.shared_store
        if collection not in store:
            store[collection] = {}
        store[collection][key] = value
        log(f"[DBManager] Set {storage}.{collection}:{key}")

    async def get(self, collection: str, key: str, storage: str = "edge") -> Any:
        store = self.edge_store if storage == "edge" else self.shared_store
        return store.get(collection, {}).get(key)

    async def delete(self, collection: str, key: str, storage: str = "edge"):
        store = self.edge_store if storage == "edge" else self.shared_store
        if collection in store and key in store[collection]:
            del store[collection][key]
            log(f"[DBManager] Deleted {storage}.{collection}:{key}")

    async def replicate_to_shared(self):
        """Copy all edge records to shared store."""
        for collection, items in self.edge_store.items():
            if collection not in self.shared_store:
                self.shared_store[collection] = {}
            self.shared_store[collection].update(items)
        log("[DBManager] Replicated edge to shared store")

# Global DB instance
db_manager = DBManager()
