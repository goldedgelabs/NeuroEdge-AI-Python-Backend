# backend-python/agents/TranslationAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class TranslationAgent:
    name = "TranslationAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def translate_text(self, text: str, target_lang: str) -> dict:
        """
        Translate the given text to the target language.
        """
        logger.log(f"[TranslationAgent] Translating text to {target_lang}: {text}")

        # Dummy translation logic (replace with real API or model)
        translated_text = f"{text} ({target_lang})"

        translation_data = {"original": text, "translated": translated_text, "target_lang": target_lang}
        await db.set("translations", f"{hash(text)}_{target_lang}", translation_data, "edge")
        eventBus.publish("db:update", {
            "collection": "translations",
            "key": f"{hash(text)}_{target_lang}",
            "value": translation_data,
            "source": self.name
        })

        logger.log(f"[TranslationAgent] Translation saved in DB")
        return translation_data

    async def handle_db_update(self, event: dict):
        logger.log(f"[TranslationAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[TranslationAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[TranslationAgent] Recovering from error: {error}")
