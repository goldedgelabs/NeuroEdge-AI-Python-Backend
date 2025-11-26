from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class ResearchAnalyticsEngine:
    name = "ResearchAnalyticsEngine"

    def __init__(self):
        self.reports = {}

    async def add_report(self, report_id: str, report_data: dict):
        """Add or update a research analytics report."""
        self.reports[report_id] = report_data

        # Save to DB and emit update event
        await db.set("research_reports", report_id, report_data, storage="edge")
        eventBus.publish("db:update", {
            "collection": "research_reports",
            "key": report_id,
            "value": report_data,
            "source": self.name
        })
        log(f"[{self.name}] Report added/updated: {report_id}")
        return report_data

    async def get_report(self, criteria: dict):
        """Retrieve reports matching criteria."""
        results = [
            r for r in self.reports.values()
            if all(r.get(k) == v for k, v in criteria.items())
        ]
        log(f"[{self.name}] Reports retrieved: {results}")
        return results

    async def remove_report(self, report_id: str):
        """Remove a report."""
        await db.delete("research_reports", report_id, storage="edge")
        eventBus.publish("db:delete", {
            "collection": "research_reports",
            "key": report_id,
            "source": self.name
        })
        log(f"[{self.name}] Removed report: {report_id}")
        self.reports.pop(report_id, None)

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
