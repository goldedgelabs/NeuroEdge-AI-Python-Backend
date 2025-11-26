# backend-python/agents/PredictionAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class PredictionAgent:
    name = "PredictionAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def predict(self, collection: str, input_data: dict) -> dict:
        """
        Generate predictions based on input data and save results.
        """
        if not input_data:
            logger.warn(f"[PredictionAgent] No input data provided")
            return {"error": "No input data provided"}

        # Example prediction logic: placeholder
        prediction_result = {k: v for k, v in input_data.items()}
        prediction_result["predicted_at"] = time.time()
        prediction_result["prediction"] = "example_prediction"

        record_id = f"prediction_{int(time.time()*1000)}"
        await db.set(collection, record_id, prediction_result, target="edge")
        eventBus.publish("db:update", {
            "collection": collection,
            "key": record_id,
            "value": prediction_result,
            "source": self.name
        })

        logger.log(f"[PredictionAgent] Prediction saved: {collection}:{record_id}")
        return {"record_id": record_id, "prediction": prediction_result["prediction"]}

    async def handle_db_update(self, event: dict):
        logger.log(f"[PredictionAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[PredictionAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[PredictionAgent] Recovering from error: {error}")
