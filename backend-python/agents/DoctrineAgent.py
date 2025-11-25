# backend-python/agents/DoctrineAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class DoctrineAgent:
    name = "DoctrineAgent"

    def __init__(self):
        # Subscribes to DB updates if needed
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)
        self.rules = {}  # Rules can be loaded dynamically

    async def enforce_action(self, action: str, folder: str = "", role: str = "user") -> dict:
        """
        Checks whether a specific action is allowed based on current doctrine rules.
        """
        rule_key = f"{folder}:{role}:{action}"
        allowed = self.rules.get(rule_key, True)
        message = "" if allowed else "Action blocked by doctrine rules."
        logger.log(f"[DoctrineAgent] Action check {action} → {allowed}")
        return {"success": allowed, "message": message}

    async def add_rule(self, folder: str, role: str, action: str, allow: bool = True):
        """
        Adds or updates a rule in the doctrine agent.
        """
        rule_key = f"{folder}:{role}:{action}"
        self.rules[rule_key] = allow
        logger.log(f"[DoctrineAgent] Rule set: {rule_key} = {allow}")
        await db.set("doctrine_rules", rule_key, {"allow": allow}, "edge")
        eventBus.publish("db:update", {"collection": "doctrine_rules", "key": rule_key, "value": {"allow": allow}, "source": self.name})

    async def handle_db_update(self, event: dict):
        logger.log(f"[DoctrineAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[DoctrineAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[DoctrineAgent] Recovering from error: {error}")
