from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class ResearchEngine:
    name = "ResearchEngine"

    def __init__(self):
        self.documents = {}

    async def add_document(self, doc_id: str, doc_data: dict):
        """Add or update a research document."""
        self.documents[doc_id] = doc_data

        # Save to DB and emit update event
        await db.set("research_documents", doc_id, doc_data, storage="edge")
        eventBus.publish("db:update", {
            "collection": "research_documents",
            "key": doc_id,
            "value": doc_data,
            "source": self.name
        })
        log(f"[{self.name}] Document added/updated: {doc_id}")
        return doc_data

    async def get_documents(self, criteria: dict):
        """Retrieve documents matching criteria."""
        results = [
            d for d in self.documents.values()
            if all(d.get(k) == v for k, v in criteria.items())
        ]
        log(f"[{self.name}] Documents retrieved: {results}")
        return results

    async def remove_document(self, doc_id: str):
        """Remove a document."""
        await db.delete("research_documents", doc_id, storage="edge")
        eventBus.publish("db:delete", {
            "collection": "research_documents",
            "key": doc_id,
            "source": self.name
        })
        log(f"[{self.name}] Removed document: {doc_id}")
        self.documents.pop(doc_id, None)

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
