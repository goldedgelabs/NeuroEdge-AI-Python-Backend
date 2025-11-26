# backend-python/core/dbManager.py
import asyncio
from utils.logger import logger

class DBManager:
    def __init__(self):
        # Simulate storage layers: edge (local) and shared (central)
        self.store = {"edge": {}, "shared": {}}

    async def set(self, collection: str, key: str, value: dict, target: str = "edge"):
        if target not in self.store:
            logger.warn(f"[DBManager] Unknown target: {target}")
            return
        self.store[target].setdefault(collection, {})[key] = value
        logger.log(f"[DBManager] {target.upper()} DB updated: {collection}:{key}")

    async def get(self, collection: str, key: str, target: str = "edge"):
        return self.store.get(target, {}).get(collection, {}).get(key)

    async def get_all(self, collection: str, target: str = "edge"):
        return list(self.store.get(target, {}).get(collection, {}).values())

    async def delete(self, collection: str, key: str, target: str = "edge"):
        coll = self.store.get(target, {}).get(collection, {})
        if key in coll:
            del coll[key]
            logger.log(f"[DBManager] {target.upper()} DB deleted: {collection}:{key}")

db = DBManager()
