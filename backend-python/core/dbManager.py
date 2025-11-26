# backend-python/core/dbManager.py

class DBManager:
    def __init__(self):
        # Each storage layer: edge or shared
        self.store = {"edge": {}, "shared": {}}

    async def set(self, collection: str, key: str, value: dict, target: str = "edge"):
        if collection not in self.store[target]:
            self.store[target][collection] = {}
        self.store[target][collection][key] = value
        return value

    async def get(self, collection: str, key: str, target: str = "edge"):
        return self.store.get(target, {}).get(collection, {}).get(key)

    async def get_all(self, collection: str, target: str = "edge"):
        return list(self.store.get(target, {}).get(collection, {}).values()) or []
