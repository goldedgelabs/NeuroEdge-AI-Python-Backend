from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
import datetime

class ConversationEngine(EngineBase):
    async def run(self, input_data):
        """
        Handles conversational input and generates structured responses.
        """
        user_input = input_data.get("text", "")
        conversation_id = input_data.get("id", f"conv_{datetime.datetime.utcnow().timestamp()}")

        # Prepare conversation record
        conversation_record = {
            "collection": "conversations",
            "id": conversation_id,
            "text": user_input,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        # Save conversation to DB
        await db.set(conversation_record["collection"], conversation_record["id"], conversation_record, "edge")

        # Publish update to event bus
        await event_bus.publish("db:update", conversation_record)

        # Here you could call a NLP module or AI model for response generation
        response_text = f"[Simulated Response] Received: {user_input}"

        conversation_record["response"] = response_text
        return conversation_record

    async def get_history(self, conversation_id: str = None):
        """
        Retrieve conversation history
        """
        all_conversations = await db.getAll("conversations", "edge")
        if conversation_id:
            return [c for c in all_conversations if c["id"] == conversation_id]
        return all_conversations
