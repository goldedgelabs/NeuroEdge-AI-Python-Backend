from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class PersonaEngine:
    name = "PersonaEngine"

    def __init__(self):
        self.personas = {}

    async def create_persona(self, persona_id: str, attributes: dict):
        """Create or update a persona."""
        persona = {
            "id": persona_id,
            "attributes": attributes
        }
        self.personas[persona_id] = persona

        # Save to DB and emit update event
        await db.set("personas", persona_id, persona, storage="edge")
        eventBus.publish("db:update", {
            "collection": "personas",
            "key": persona_id,
            "value": persona,
            "source": self.name
        })
        log(f"[{self.name}] Created/Updated persona: {persona_id}")
        return persona

    async def get_persona(self, persona_id: str):
        """Retrieve a persona."""
        return await db.get("personas", persona_id, storage="edge")

    async def delete_persona(self, persona_id: str):
        """Delete a persona."""
        await db.delete("personas", persona_id, storage="edge")
        eventBus.publish("db:delete", {
            "collection": "personas",
            "key": persona_id,
            "source": self.name
        })
        log(f"[{self.name}] Deleted persona: {persona_id}")
        self.personas.pop(persona_id, None)

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
