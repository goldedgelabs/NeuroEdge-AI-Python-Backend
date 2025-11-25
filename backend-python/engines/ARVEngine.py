# ARVEngine.py
from core.db_manager import DBManager
from core.event_bus import EventBus
from core.logger import logger

class ARVEngine:
    name = "ARVEngine"

    def __init__(self):
        self.db = DBManager()
        self.event_bus = EventBus()
        logger.log(f"[ARVEngine] Initialized {self.name}")

    async def run(self, input_data: dict):
        """
        Main entry for the engine.
        Example input_data: {"patient_id": "123", "action": "analyze"}
        """
        try:
            result = await self.analyze_patient(input_data)
            
            # DB integration
            if "collection" in result and "id" in result:
                await self.db.set(result["collection"], result["id"], result)
                self.event_bus.publish("db:update", {
                    "collection": result["collection"],
                    "key": result["id"],
                    "value": result,
                    "source": self.name
                })
                logger.log(f"[ARVEngine] DB updated → {result['collection']}:{result['id']}")
            
            return result
        except Exception as e:
            logger.error(f"[ARVEngine] Error in run: {e}")
            if hasattr(self, "recover"):
                return await self.recover(e)
            return {"error": "Failed to process ARVEngine run"}

    async def analyze_patient(self, data: dict):
        """
        Example processing logic.
        """
        patient_id = data.get("patient_id")
        # Placeholder: actual ARV analysis logic
        result = {
            "collection": "patients",
            "id": patient_id,
            "status": "analyzed",
            "details": {"notes": "ARV analysis completed"}
        }
        return result

    async def recover(self, error):
        """
        Optional recovery method if something fails.
        """
        logger.warn(f"[ARVEngine] Recovering from error: {error}")
        return {"error": "Recovered from ARVEngine failure"}
