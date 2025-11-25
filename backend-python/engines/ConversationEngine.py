from db.db_manager import db_manager
from utils.logger import log

class ConversationEngine:
    name = "ConversationEngine"

    async def run(self, input_data=None):
        log(f"[{self.name}] Processing conversation: {input_data}")
        # Example conversation processing
        response = {
            "collection": "conversations",
            "id": input_data.get("id") if input_data else "default",
            "message": f"Processed input: {input_data}"
        }
        await db_manager.set(response["collection"], response["id"], response)
        return response

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
