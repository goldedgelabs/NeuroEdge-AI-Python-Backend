from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class ReasoningEngine:
    name = "ReasoningEngine"

    def __init__(self):
        self.knowledge_base = {}

    async def add_fact(self, fact_id: str, fact_data: dict):
        """Add or update a fact in the knowledge base."""
        self.knowledge_base[fact_id] = fact_data

        # Save to DB and emit update event
        await db.set("reasoning_facts", fact_id, fact_data, storage="edge")
        eventBus.publish("db:update", {
            "collection": "reasoning_facts",
            "key": fact_id,
            "value": fact_data,
            "source": self.name
        })
        log(f"[{self.name}] Fact added/updated: {fact_id}")
        return fact_data

    async def infer(self, query: str):
        """Perform simple reasoning over stored facts."""
        # Example: return facts containing the query string
        results = {k: v for k, v in self.knowledge_base.items() if query.lower() in str(v).lower()}
        log(f"[{self.name}] Inference for query '{query}': {results}")
        return results

    async def remove_fact(self, fact_id: str):
        """Remove a fact from the knowledge base."""
        await db.delete("reasoning_facts", fact_id, storage="edge")
        eventBus.publish("db:delete", {
            "collection": "reasoning_facts",
            "key": fact_id,
            "source": self.name
        })
        log(f"[{self.name}] Removed fact: {fact_id}")
        self.knowledge_base.pop(fact_id, None)

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
