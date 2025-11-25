from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
from utils.logger import logger

class MarketEngine(EngineBase):
    """
    Handles market analysis, pricing, trends, and predictions.
    """

    async def add_market_data(self, market_id: str, data: dict):
        """
        Add or update market data.
        """
        record_data = {
            "id": market_id,
            "collection": "market",
            "data": data
        }

        # Write to DB
        await db.set("market", market_id, record_data, "edge")
        await event_bus.publish("db:update", {
            "collection": "market",
            "key": market_id,
            "value": record_data,
            "source": "MarketEngine"
        })

        logger.log(f"[MarketEngine] Market data updated: {market_id}")
        return record_data

    async def get_market_data(self, market_id: str):
        """
        Retrieve market data from edge DB.
        """
        record = await db.get("market", market_id, "edge")
        logger.log(f"[MarketEngine] Retrieved market data: {market_id}")
        return record

    async def run(self, input_data: dict):
        """
        Main entry point:
        {
            "action": "add" | "get",
            "market_id": str,
            "data": dict (optional)
        }
        """
        action = input_data.get("action")
        market_id = input_data.get("market_id")

        if action == "add":
            data = input_data.get("data", {})
            return await self.add_market_data(market_id, data)
        elif action == "get":
            return await self.get_market_data(market_id)
        else:
            return {"error": f"Unknown action: {action}"}
