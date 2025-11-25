from db.db_manager import db_manager
from utils.logger import log

class AnalyticsEngine:
    name = "AnalyticsEngine"

    async def run(self, input_data=None):
        log(f"[{self.name}] Running with input: {input_data}")
        # Example processing
        result = {
            "collection": "analytics",
            "id": input_data.get("id") if input_data else "default",
            "data": input_data
        }
        # Write to DB automatically
        await db_manager.set(result["collection"], result["id"], result)
        return result

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
