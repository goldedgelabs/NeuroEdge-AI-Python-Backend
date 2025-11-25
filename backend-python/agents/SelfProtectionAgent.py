# backend-python/agents/SelfProtectionAgent.py
from core.AgentBase import AgentBase
from utils.logger import logger
from db.dbManager import db
import time

class SelfProtectionAgent(AgentBase):
    name = "SelfProtectionAgent"

    async def handle(self, task: dict):
        """
        Handles internal safety, anomaly detection, and auto-defense actions.
        """
        try:
            action = task.get("action")

            if action == "detect_anomaly":
                return await self.detect_anomaly(task.get("data"))

            elif action == "log_threat":
                return await self.log_threat(task.get("details"))

            elif action == "get_threats":
                return await self.get_threats()

            elif action == "auto_recover":
                return await self.auto_recover(task.get("error"))

            else:
                return {"error": "Unknown action for SelfProtectionAgent"}

        except Exception as e:
            logger.error(f"[SelfProtectionAgent] ERROR: {e}")
            return {"error": str(e)}

    async def detect_anomaly(self, data: dict):
        """
        Detects anomalies in engine/agent behavior.
        Example signals:
        - unusually long execution time
        - repeated failures
        - unauthorized access patterns
        """
        if not data:
            return {"error": "Missing anomaly data"}

        flagged = []

        if data.get("execution_time") and data["execution_time"] > 3:
            flagged.append("Slow execution time detected")

        if data.get("failures") and data["failures"] > 3:
            flagged.append("Multiple consecutive failures")

        if data.get("unauthorized") is True:
            flagged.append("Unauthorized action attempt detected")

        result = {
            "timestamp": time.time(),
            "anomalies": flagged or ["No anomalies"]
        }

        record_id = f"anom_{int(time.time()*1000)}"
        await db.set("self_protection_logs", record_id, result)

        return {"id": record_id, "result": result}

    async def log_threat(self, details: dict):
        """
        Store a threat report in DB.
        """
        if not details:
            return {"error": "Missing threat details"}

        entry = {
            "timestamp": time.time(),
            "type": details.get("type", "unknown"),
            "description": details.get("description", "No description"),
            "severity": details.get("severity", "low"),
        }

        threat_id = f"threat_{int(time.time()*1000)}"
        await db.set("threat_logs", threat_id, entry)

        return {"status": "logged", "id": threat_id}

    async def get_threats(self):
        """
        Returns all threat logs.
        """
        logs = await db.get_all("threat_logs") or []
        return {"count": len(logs), "logs": logs}

    async def auto_recover(self, error: dict):
        """
        Attempts to automatically recover from a system fault.
        """
        if not error:
            return {"error": "Missing error details"}

        logger.warn(f"[SelfProtectionAgent] Auto-recovery triggered: {error}")

        recovery_log = {
            "timestamp": time.time(),
            "error": error,
            "status": "recovered"
        }

        recovery_id = f"recovery_{int(time.time()*1000)}"
        await db.set("auto_recovery_logs", recovery_id, recovery_log)

        return {"status": "auto_recovered", "id": recovery_id}
