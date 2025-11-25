# ResearchAnalyticsAgent.py
from core.agent_base import AgentBase
from db.db_manager import DBManager
from core.event_bus import EventBus

class ResearchAnalyticsAgent(AgentBase):
    name = "ResearchAnalyticsAgent"

    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.event_bus = EventBus()

        # Subscribe to DB updates automatically
        self.event_bus.subscribe("db:update", self.handle_db_update)
        self.event_bus.subscribe("db:delete", self.handle_db_delete)

    async def process_new_research(self, data: dict):
        """
        Process incoming research data
        """
        research_id = data.get("id")
        collection = "research_analytics"

        record = {
            "id": research_id,
            "collection": collection,
            "data": data,
        }

        # Save to DB
        await self.db.set(collection, research_id, record, storage="edge")

        # Emit DB event
        self.event_bus.publish("db:update", {
            "collection": collection,
            "key": research_id,
            "value": record,
            "source": self.name
        })

        return record

    async def handle_db_update(self, event: dict):
        """
        Handle DB updates
        """
        collection = event.get("collection")
        if collection == "research":
            await self.process_new_research(event.get("value"))

    async def handle_db_delete(self, event: dict):
        """
        Handle DB deletes
        """
        collection = event.get("collection")
        key = event.get("key")
        print(f"[ResearchAnalyticsAgent] Deleted record {collection}:{key}")

    async def recover(self, error: Exception):
        """
        Graceful recovery
        """
        print(f"[ResearchAnalyticsAgent] Recovered from error: {error}")
        return {"error": str(error)}

# Optional direct test
if __name__ == "__main__":
    import asyncio
    agent = ResearchAnalyticsAgent()
    test_data = {"id": "research1", "title": "Test Research", "metrics": [1,2,3]}
    result = asyncio.run(agent.process_new_research(test_data))
    print(result)
