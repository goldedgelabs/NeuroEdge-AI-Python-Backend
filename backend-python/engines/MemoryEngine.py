from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
import datetime

class MemoryEngine(EngineBase):
    async def run(self, input_data):
        """
        Handles storing and retrieving long-term and short-term memory
        for NeuroEdge system operations.
        """
        memory_type = input_data.get("type", "short-term")  # short-term or long-term
        content = input_data.get("content", "")
        memory_id = input_data.get("id", f"mem_{datetime.datetime.utcnow().timestamp()}")

        # Prepare memory record
        memory_record = {
            "collection": "memory",
            "id": memory_id,
            "type": memory_type,
            "content": content,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        # Save memory to DB
        await db.set(memory_record["collection"], memory_record["id"], memory_record, "edge")

        # Publish update to event bus for other agents/engines
        await event_bus.publish("db:update", memory_record)

        return memory_record

    async def recall(self, query: str):
        """
        Simple retrieval based on query string
        """
        all_memories = await db.getAll("memory", "edge")
        results = [m for m in all_memories if query.lower() in m.get("content", "").lower()]
        return results
