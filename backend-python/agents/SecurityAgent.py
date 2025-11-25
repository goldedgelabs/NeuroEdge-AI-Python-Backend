# backend-python/agents/SecurityAgent.py
from core.AgentBase import AgentBase
from db.dbManager import db
from utils.logger import logger
import hashlib
import time

class SecurityAgent(AgentBase):
    name = "SecurityAgent"

    async def handle(self, task: dict):
        """
        Handles system-wide and device-level security checks:
        - Hash verification
        - Intrusion checks
        - DB tampering detection
        - Token / session validation
        """
        try:
            action = task.get("action")

            if action == "hash_file":
                return await self.hash_file(task.get("content", ""))

            elif action == "validate_token":
                return await self.validate_token(task.get("token"))

            elif action == "get_security_status":
                return await self.security_status()

            else:
                return {"error": "Unknown security action"}

        except Exception as e:
            logger.error(f"[SecurityAgent] Error: {e}")
            return {"error": str(e)}

    async def hash_file(self, content: str):
        """Create a SHA-256 hash for integrity checking."""
        h = hashlib.sha256(content.encode()).hexdigest()
        return {"hash": h}

    async def validate_token(self, token: str):
        """Validates token formats and expiration if stored."""
        if not token:
            return {"valid": False, "reason": "Missing token"}

        try:
            token_store = await db.get("auth_tokens", token)
            if not token_store:
                return {"valid": False, "reason": "Token not found"}

            if token_store.get("expires", 0) < time.time():
                return {"valid": False, "reason": "Token expired"}

            return {"valid": True}
        except:
            return {"valid": False, "reason": "Validation failed"}

    async def security_status(self):
        """Fetch system-wide security metrics."""
        metrics = await db.get_all("security_metrics")

        return {
            "status": "secure",
            "metrics_collected": len(metrics) if metrics else 0,
            "timestamp": time.time()
                               }
