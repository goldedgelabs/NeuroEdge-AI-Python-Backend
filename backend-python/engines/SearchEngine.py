from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus

class SearchEngine(EngineBase):
    """
    Handles searching through various datasets: documents, logs, agents, and engine outputs.
    """

    async def search_collection(self, collection: str, query: dict):
        """
        Search a specific collection based on query criteria.
        """
        results = []
        all_records = await db.get_all(collection, "edge")
        for record in all_records:
            match = all(
                record.get(k) == v for k, v in query.items()
            )
            if match:
                results.append(record)
        return results

    async def index_record(self, collection: str, record: dict):
        """
        Add/update a record in the collection and emit DB event.
        """
        await db.set(collection, record["id"], record, "edge")
        await event_bus.publish("db:update", {
            "collection": collection,
            "key": record["id"],
            "value": record,
            "source": "SearchEngine"
        })

    async def run(self, input_data: dict):
        """
        Main entry point for search engine.
        input_data can have:
        {
            "action": "search" | "index",
            "collection": str,
            "query": dict,
            "record": dict
        }
        """
        action = input_data.get("action")
        collection = input_data.get("collection")
        if action == "search":
            query = input_data.get("query", {})
            return await self.search_collection(collection, query)
        elif action == "index":
            record = input_data.get("record")
            return await self.index_record(collection, record)
        else:
            return {"error": f"Unknown action: {action}"}
