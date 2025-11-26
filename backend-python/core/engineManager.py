# backend-python/core/engineManager.py
from .dbManager import db
from .eventBus import eventBus
from .logger import logger

# Import all 42 engines
from ..engines import *  # Assuming __init__.py exports all engines

engineManager = {}

def register_engine(name: str, instance):
    engineManager[name] = instance
    logger.log(f"[EngineManager] Registered engine: {name}")

# Auto-register all engines
from ..engines import (
    AREngine, AnalyticsEngine, CodeEngine, ConversationEngine, CreativityEngine,
    CriticEngine, DataIngestEngine, DataInspectEngine, DeviceProtectionEngine,
    DoctrineEngine, EdgeDeviceEngine, GamingCreativeEngine, GoldEdgeIntegrationEngine,
    HealthEngine, MarketEngine, MedicineManagementEngine, MemoryEngine, MonitoringEngine,
    MultiModalEngine, OrchestrationEngine, PersonaEngine, PhoneSecurityEngine,
    PlannerEngine, PolicyEngine, PredictiveEngine, RealTimeRecommenderEngine,
    ReasoningEngine, RecommendationEngine, ReinforcementEngine, ResearchAnalyticsEngine,
    ResearchEngine, SchedulerEngine, SchedulingEngine, SearchEngine, SecurityEngine,
    SelfImprovementEngine, SimulationEngine, SummarizationEngine, TelemetryEngine,
    TranslationEngine, VisionEngine, VoiceEngine
)

for EngineClass in [
    AREngine, AnalyticsEngine, CodeEngine, ConversationEngine, CreativityEngine,
    CriticEngine, DataIngestEngine, DataInspectEngine, DeviceProtectionEngine,
    DoctrineEngine, EdgeDeviceEngine, GamingCreativeEngine, GoldEdgeIntegrationEngine,
    HealthEngine, MarketEngine, MedicineManagementEngine, MemoryEngine, MonitoringEngine,
    MultiModalEngine, OrchestrationEngine, PersonaEngine, PhoneSecurityEngine,
    PlannerEngine, PolicyEngine, PredictiveEngine, RealTimeRecommenderEngine,
    ReasoningEngine, RecommendationEngine, ReinforcementEngine, ResearchAnalyticsEngine,
    ResearchEngine, SchedulerEngine, SchedulingEngine, SearchEngine, SecurityEngine,
    SelfImprovementEngine, SimulationEngine, SummarizationEngine, TelemetryEngine,
    TranslationEngine, VisionEngine, VoiceEngine
]:
    register_engine(EngineClass.__name__, EngineClass())
