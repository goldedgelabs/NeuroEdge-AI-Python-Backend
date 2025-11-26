from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class ReinforcementEngine:
    name = "ReinforcementEngine"

    def __init__(self):
        self.policies = {}

    async def add_policy(self, policy_id: str, policy_data: dict):
        """Add or update a reinforcement policy."""
        self.policies[policy_id] = policy_data

        # Save to DB and emit update event
        await db.set("policies", policy_id, policy_data, storage="edge")
        eventBus.publish("db:update", {
            "collection": "policies",
            "key": policy_id,
            "value": policy_data,
            "source": self.name
        })
        log(f"[{self.name}] Policy added/updated: {policy_id}")
        return policy_data

    async def get_policy(self, criteria: dict):
        """Retrieve policies matching criteria."""
        results = [
            p for p in self.policies.values()
            if all(p.get(k) == v for k, v in criteria.items())
        ]
        log(f"[{self.name}] Policies retrieved: {results}")
        return results

    async def remove_policy(self, policy_id: str):
        """Remove a policy."""
        await db.delete("policies", policy_id, storage="edge")
        eventBus.publish("db:delete", {
            "collection": "policies",
            "key": policy_id,
            "source": self.name
        })
        log(f"[{self.name}] Removed policy: {policy_id}")
        self.policies.pop(policy_id, None)

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
