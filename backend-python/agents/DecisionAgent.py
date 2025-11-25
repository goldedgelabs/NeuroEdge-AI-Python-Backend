# backend-python/agents/DecisionAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import asyncio

class DecisionAgent:
    name = "DecisionAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def make_decision(self, input_data: dict):
        """
        Simple decision-making logic based on input_data.
        """
        try:
            # Example decision: pick action based on priority
            actions = input_data.get("actions", [])
            if not actions:
                return {"error": "no_actions_provided"}
            
            # Priority-based decision (higher 'priority' wins)
            selected = max(actions, key=lambda a: a.get("priority", 0))
            
            # Optionally, log the decision
            logger.log(f"[DecisionAgent] Decision made: {selected}")

            # Save to DB
            record_id = input_data.get("id", "decision_temp")
            await db.set("decisions", record_id, selected, target="edge")
            eventBus.publish("db:update", {
                "collection": "decisions",
                "key": record_id,
                "value": selected,
                "source": self.name
            })

            return selected
        except Exception as e:
            await self.recover(e)
            return {"error": "decision_failed"}

    async def handle_db_update(self, event: dict):
        logger.log(f"[DecisionAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[DecisionAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[DecisionAgent] Recovering from error: {error}")
