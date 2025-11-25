from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus

class DataIngestEngine(EngineBase):
    async def run(self, input_data):
        """
        Handles ingestion of raw data from various sources (APIs, files, sensors),
        cleans it, and stores it in the edge database.
        """
        source = input_data.get("source")
        raw_data = input_data.get("data", {})

        try:
            # Placeholder: implement data cleaning/processing logic here
            cleaned_data = {k: v for k, v in raw_data.items() if v is not None}
        except Exception as e:
            cleaned_data = {"error": str(e)}

        result = {
            "collection": "data_ingest",
            "id": input_data.get("id", "default_data"),
            "data": cleaned_data,
            "source": source
        }

        # Save to DB and notify subscribers
        await db.set(result["collection"], result["id"], result, "edge")
        await event_bus.publish("db:update", result)

        return result
