from db.db_manager import db_manager
from utils.logger import log

class DataIngestEngine:
    name = "DataIngestEngine"

    async def run(self, input_data=None):
        log(f"[{self.name}] Ingesting data: {input_data}")
        # Example data ingestion process
        result = {
            "collection": "data_ingest",
            "id": input_data.get("id") if input_data else "default",
            "data": input_data
        }
        await db_manager.set(result["collection"], result["id"], result)
        return result

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
