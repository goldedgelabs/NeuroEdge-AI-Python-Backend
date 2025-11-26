# backend-python/agents/SecurityAuditAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class SecurityAuditAgent:
    name = "SecurityAuditAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def audit_security(self, collection: str) -> dict:
        """
        Perform a security audit on the specified collection.
        """
        records = await db.get_all(collection, target="edge") or []
        audit_results = []

        for record in records:
            issues = []
            if "password" in record:
                issues.append("Password field present")
            if record.get("role") == "admin" and not record.get("2fa_enabled"):
                issues.append("Admin without 2FA")
            audit_results.append({
                "key": record.get("id"),
                "issues": issues or ["No issues"]
            })

        result = {
            "timestamp": time.time(),
            "collection": collection,
            "audit_results": audit_results
        }

        record_id = f"audit_{int(time.time()*1000)}"
        await db.set("security_audits", record_id, result, target="edge")
        eventBus.publish("db:update", {
            "collection": "security_audits",
            "key": record_id,
            "value": result,
            "source": self.name
        })

        logger.log(f"[SecurityAuditAgent] Security audit saved: security_audits:{record_id}")
        return result

    async def handle_db_update(self, event: dict):
        logger.log(f"[SecurityAuditAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[SecurityAuditAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[SecurityAuditAgent] Recovering from error: {error}")
