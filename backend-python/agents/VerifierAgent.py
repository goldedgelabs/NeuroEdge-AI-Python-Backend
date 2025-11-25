# backend-python/agents/VerifierAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class VerifierAgent:
    name = "VerifierAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def verify_record(self, collection: str, key: str) -> dict:
        """
        Verifies a DB record against a set of rules or standards.
        """
        record = await db.get(collection, key)
        if not record:
            logger.warn(f"[VerifierAgent] Record not found: {collection}:{key}")
            return {"verified": False, "reason": "Record not found"}

        # Example verification logic
        verified = True
        errors = []
        if "id" not in record or "collection" not in record:
            verified = False
            errors.append("Missing required fields")

        verification_result = {
            "collection": collection,
            "key": key,
            "verified": verified,
            "errors": errors
        }

        # Save verification result to DB
        await db.set("verification", f"{collection}_{key}", verification_result, "edge")
        eventBus.publish("db:update", {
            "collection": "verification",
            "key": f"{collection}_{key}",
            "value": verification_result,
            "source": self.name
        })

        logger.log(f"[VerifierAgent] Verification result saved for {collection}:{key}")
        return verification_result

    async def handle_db_update(self, event: dict):
        logger.log(f"[VerifierAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[VerifierAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[VerifierAgent] Recovering from error: {error}")
