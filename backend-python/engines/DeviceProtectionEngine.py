from db.db_manager import db_manager
from utils.logger import log

class DeviceProtectionEngine:
    name = "DeviceProtectionEngine"

    async def run(self, input_data=None):
        log(f"[{self.name}] Protecting devices with input: {input_data}")
        # Example protection logic
        result = {
            "collection": "device_protection",
            "id": input_data.get("id") if input_data else "default",
            "status": "secured",
            "details": input_data
        }
        await db_manager.set(result["collection"], result["id"], result)
        return result

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
