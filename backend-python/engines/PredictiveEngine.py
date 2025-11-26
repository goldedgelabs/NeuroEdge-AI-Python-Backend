from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class PredictiveEngine:
    name = "PredictiveEngine"

    def __init__(self):
        self.models = {}

    async def train_model(self, model_id: str, data: dict):
        """Train or update a predictive model."""
        # Simplified: just store the data
        self.models[model_id] = data

        # Save to DB and emit update event
        await db.set("predictive_models", model_id, data, storage="edge")
        eventBus.publish("db:update", {
            "collection": "predictive_models",
            "key": model_id,
            "value": data,
            "source": self.name
        })
        log(f"[{self.name}] Model trained/updated: {model_id}")
        return data

    async def predict(self, model_id: str, input_data: dict):
        """Run prediction based on stored model data."""
        model = self.models.get(model_id)
        if not model:
            return {"error": "Model not found"}

        # Simplified prediction logic (echo input + model summary)
        prediction = {"input": input_data, "model_summary": model}
        log(f"[{self.name}] Prediction using {model_id}: {prediction}")
        return prediction

    async def delete_model(self, model_id: str):
        """Delete a predictive model."""
        await db.delete("predictive_models", model_id, storage="edge")
        eventBus.publish("db:delete", {
            "collection": "predictive_models",
            "key": model_id,
            "source": self.name
        })
        log(f"[{self.name}] Deleted model: {model_id}")
        self.models.pop(model_id, None)

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
