from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus


class MarketEngine:
    name = "MarketEngine"

    def __init__(self):
        self.records = {}

    async def analyze_market(self, record_id: str, market_data: dict):
        """Analyze market data and produce insights."""
        insights = self._generate_insights(market_data)

        data = {
            "id": record_id,
            "market_data": market_data,
            "insights": insights
        }

        # Save to DB
        await db.set("market_records", record_id, data, storage="edge")

        # Emit replication event
        eventBus.publish("db:update", {
            "collection": "market_records",
            "key": record_id,
            "value": data,
            "source": self.name
        })

        log(f"[{self.name}] Market analysis complete for record {record_id}")
        return data

    async def update_record(self, record_id: str, patch: dict):
        """Update existing market record."""
        existing = await db.get("market_records", record_id, storage="edge") or {}

        updated = {**existing, **patch}
        updated["id"] = record_id

        await db.set("market_records", record_id, updated, storage="edge")

        eventBus.publish("db:update", {
            "collection": "market_records",
            "key": record_id,
            "value": updated,
            "source": self.name
        })

        log(f"[{self.name}] Market record updated: {record_id}")
        return updated

    async def remove_record(self, record_id: str):
        """Remove a market record."""
        await db.delete("market_records", record_id)

        eventBus.publish("db:delete", {
            "collection": "market_records",
            "key": record_id,
            "source": self.name
        })

        log(f"[{self.name}] Market record removed: {record_id}")
        return {"success": True, "id": record_id}

    def _generate_insights(self, market_data: dict):
        """Simple insight generation logic."""
        price = market_data.get("price", 0)
        trend = market_data.get("trend", "stable")

        if price > 1000 and trend == "up":
            return "high_growth"
        if price < 200 and trend == "down":
            return "risk_alert"
        return "stable"

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
