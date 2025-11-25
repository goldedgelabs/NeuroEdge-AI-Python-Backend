from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
import datetime

class SecurityEngine(EngineBase):
    async def run(self, input_data):
        """
        Performs security analysis on devices, users, or activities.
        """
        target_id = input_data.get("target_id", "unknown")
        check_type = input_data.get("check_type", "basic")
        analysis_id = f"sec_{target_id}_{int(datetime.datetime.utcnow().timestamp())}"

        # Example: dummy security check
        findings = {"status": "safe", "issues": []}
        if check_type == "advanced":
            findings["issues"] = ["example_issue_1"]

        security_record = {
            "collection": "security_checks",
            "id": analysis_id,
            "target_id": target_id,
            "check_type": check_type,
            "findings": findings,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        # Save to DB
        await db.set(security_record["collection"], security_record["id"], security_record, "edge")

        # Publish event
        await event_bus.publish("db:update", security_record)

        return security_record

    async def get_security_status(self, target_id):
        """
        Retrieve the latest security report for a target
        """
        all_reports = await db.getAll("security_checks", "edge")
        return [r for r in all_reports if r["target_id"] == target_id]
