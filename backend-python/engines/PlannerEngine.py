from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus

class PlannerEngine(EngineBase):
    async def run(self, input_data):
        """
        Creates structured plans based on goals and constraints.
        Can interact with other engines and agents to fetch required data.
        """
        goal = input_data.get("goal", "default_goal")
        constraints = input_data.get("constraints", {})

        # Basic example: create steps based on goal
        plan_steps = [
            {"step": 1, "action": f"Analyze goal '{goal}'"},
            {"step": 2, "action": "Gather required data from AnalyticsEngine"},
            {"step": 3, "action": "Draft initial plan"},
            {"step": 4, "action": "Validate with Doctrine rules"}
        ]

        # Incorporate any constraints if provided
        if constraints.get("priority"):
            plan_steps.append({"step": 5, "action": f"Adjust plan based on priority {constraints['priority']}"})

        result = {
            "collection": "plans",
            "id": input_data.get("id", "plan_default"),
            "goal": goal,
            "steps": plan_steps
        }

        # Save to DB and notify subscribers
        await db.set(result["collection"], result["id"], result, "edge")
        await event_bus.publish("db:update", result)

        return result
