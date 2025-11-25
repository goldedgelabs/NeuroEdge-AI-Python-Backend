# backend-python/agents/OrchestrationAgent.py

from core.agent_base import AgentBase
from core.db_manager import db
from core.event_bus import event_bus
from utils.logger import logger

class OrchestrationAgent(AgentBase):
    name = "OrchestrationAgent"

    def __init__(self):
        super().__init__()

    async def coordinate_engines(self, engine_tasks: list):
        """
        Receives a list of engine tasks and orchestrates their execution.
        engine_tasks: List[dict] - each dict contains {'engine_name': str, 'input': dict}
        """
        results = []
        for task in engine_tasks:
            engine_name = task.get("engine_name")
            input_data = task.get("input", {})
            engine = getattr(self, f"{engine_name}", None)
            if engine:
                try:
                    result = await engine.run(input_data)
                    results.append({engine_name: result})
                except Exception as e:
                    logger.error(f"[{self.name}] Engine {engine_name} failed: {e}")
                    results.append({engine_name: {"error": str(e)}})
            else:
                logger.warn(f"[{self.name}] Engine {engine_name} not found.")
                results.append({engine_name: {"error": "Engine not found"}})
        return results

    async def handleDBUpdate(self, data):
        """
        Optional: Respond to DB updates if orchestration depends on data changes.
        """
        logger.log(f"[{self.name}] DB update received: {data}")

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] OrchestrationAgent error: {error}")
