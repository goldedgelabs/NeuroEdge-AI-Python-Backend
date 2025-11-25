from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
from translation_service import translate_text  # Assume a translation module/service

class TranslationEngine(EngineBase):
    async def run(self, input_data):
        """
        Translates text from source language to target language.
        """
        text = input_data.get("text", "")
        source_lang = input_data.get("source_lang", "en")
        target_lang = input_data.get("target_lang", "en")

        translated_text = await translate_text(text, source_lang, target_lang)

        translation_id = input_data.get("id", f"translation_{hash(text)}")
        record = {
            "collection": "translations",
            "id": translation_id,
            "text": text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }

        # Save to DB
        await db.set(record["collection"], record["id"], record, "edge")

        # Publish event
        await event_bus.publish("db:update", record)

        return record

    async def bulk_translate(self, texts: list, source_lang="en", target_lang="en"):
        """
        Translate multiple texts asynchronously.
        """
        results = []
        for t in texts:
            result = await self.run({"text": t, "source_lang": source_lang, "target_lang": target_lang})
            results.append(result)
        return results
