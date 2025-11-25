from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
from summarization_service import summarize_text  # Assume a text summarization module/service

class SummarizationEngine(EngineBase):
    async def run(self, input_data):
        """
        Summarizes a given text.
        """
        text = input_data.get("text", "")
        summary_id = input_data.get("id", f"summary_{hash(text)}")

        summary = await summarize_text(text)

        record = {
            "collection": "summaries",
            "id": summary_id,
            "text": text,
            "summary": summary
        }

        # Save to DB
        await db.set(record["collection"], record["id"], record, "edge")

        # Publish DB update
        await event_bus.publish("db:update", record)

        return record

    async def bulk_summarize(self, texts: list):
        """
        Summarize multiple texts asynchronously.
        """
        results = []
        for t in texts:
            result = await self.run({"text": t})
            results.append(result)
        return results
