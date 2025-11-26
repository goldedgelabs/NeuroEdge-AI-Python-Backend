# backend-python/core/agentManager.py
from ..db.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

agentManager = {}

def register_agent(name: str, agent_instance):
    agentManager[name] = agent_instance
