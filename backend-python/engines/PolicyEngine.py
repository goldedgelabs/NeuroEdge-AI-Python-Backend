from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class PolicyEngine:
    name = "PolicyEngine"

    def __init__(self):
        self.policies = {}

    async def create_policy(self, policy_id: str, policy_data: dict):
        """Add or update a policy."""
        self.policies[policy_id] = policy_data

        # Save to DB and emit update event
        await db.set("policies", policy_id, policy_data, storage="edge")
        eventBus.publish("db:update", {
            "collection": "policies",
            "key": policy_id,
            "value": policy_data,
            "source": self.name
        })
        log(f"[{self.name}] Policy created/updated: {policy_id}")
        return policy_data

    async def enforce_policy(self, policy_id: str, context: dict):
        """Check if a context satisfies a policy."""
        policy = self.policies.get(policy_id)
        if not policy:
            return {"error": "Policy not found"}

        # Simplified enforcement logic
        allowed = all(context.get(k) == v for k, v in policy.items())
        log(f"[{self.name}] Enforcement check for {policy_id}: {allowed}")
        return {"policy_id": policy_id, "allowed": allowed}

    async def delete_policy(self, policy_id: str):
        """Delete policy from system."""
        await db.delete("policies", policy_id, storage="edge")
        eventBus.publish("db:delete", {
            "collection": "policies",
            "key": policy_id,
            "source": self.name
        })
        log(f"[{self.name}] Deleted policy: {policy_id}")
        self.policies.pop(policy_id, None)

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
