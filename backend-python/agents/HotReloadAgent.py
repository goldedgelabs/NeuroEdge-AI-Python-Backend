# backend-python/agents/HotReloadAgent.py

from core.agent_base import AgentBase
from core.db_manager import db
from core.event_bus import event_bus
from utils.logger import logger
import importlib
import sys
import os

class HotReloadAgent(AgentBase):
    name = "HotReloadAgent"

    def __init__(self):
        super().__init__()

    async def reload_module(self, module_name: str):
        """
        Dynamically reload a Python module for live updates.
        """
        try:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
                logger.log(f"[{self.name}] Module reloaded: {module_name}")
            else:
                __import__(module_name)
                logger.log(f"[{self.name}] Module imported for the first time: {module_name}")

            # Optional: publish a DB or event update after reload
            event_bus.publish("module:reloaded", {"module": module_name, "source": self.name})
            return {"success": True, "module": module_name}
        except Exception as e:
            await self.recover(e)
            return {"success": False, "error": str(e)}

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] HotReloadAgent encountered an error: {error}")
