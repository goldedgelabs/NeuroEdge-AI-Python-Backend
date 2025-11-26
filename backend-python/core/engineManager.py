# backend-python/core/engineManager.py

from .dbManager import db
from .eventBus import eventBus
from .logger import logger

# --- import all 42 engines ---
from ..engines.ARVEngine import ARVEngine
from ..engines.AnalyticsEngine import AnalyticsEngine
from ..engines.CodeEngine import CodeEngine
from ..engines.ConversationEngine import ConversationEngine
from ..engines.CreativityEngine import CreativityEngine
from ..engines.CriticEngine import CriticEngine
from ..engines.DataIngestEngine import DataIngestEngine
from ..engines.DataInspectEngine import DataInspectEngine
from ..engines.DeviceProtectionEngine import DeviceProtectionEngine
from ..engines.DoctrineEngine import DoctrineEngine
from ..engines.EdgeDeviceEngine import EdgeDeviceEngine
from ..engines.GamingCreativeEngine import GamingCreativeEngine
from ..engines.GoldEdgeIntegrationEngine import GoldEdgeIntegrationEngine
from ..engines.HealthEngine import HealthEngine
from ..engines.MarketEngine import MarketEngine
from ..engines.MedicineManagementEngine import MedicineManagementEngine
from ..engines.MemoryEngine import MemoryEngine
from ..engines.MonitoringEngine import MonitoringEngine
from ..engines.MultiModalEngine import MultiModalEngine
from ..engines.OrchestrationEngine import OrchestrationEngine
from ..engines.PersonaEngine import PersonaEngine
from ..engines.PhoneSecurityEngine import PhoneSecurityEngine
from ..engines.PlannerEngine import PlannerEngine
from ..engines.PolicyEngine import PolicyEngine
from ..engines.PredictiveEngine import PredictiveEngine
from ..engines.RealTimeRecommenderEngine import RealTimeRecommenderEngine
from ..engines.ReasoningEngine import ReasoningEngine
from ..engines.RecommendationEngine import RecommendationEngine
from ..engines.ReinforcementEngine import ReinforcementEngine
from ..engines.ResearchAnalyticsEngine import ResearchAnalyticsEngine
from ..engines.ResearchEngine import ResearchEngine
from ..engines.SchedulerEngine import SchedulerEngine
from ..engines.SchedulingEngine import SchedulingEngine
from ..engines.SearchEngine import SearchEngine
from ..engines.SecurityEngine import SecurityEngine
from ..engines.SelfImprovementEngine import SelfImprovementEngine
from ..engines.SimulationEngine import SimulationEngine
from ..engines.SummarizationEngine import SummarizationEngine
from ..engines.TelemetryEngine import TelemetryEngine
from ..engines.TranslationEngine import TranslationEngine
from ..engines.VisionEngine import VisionEngine
from ..engines.VoiceEngine import VoiceEngine

engineManager = {}

def register_engine(name: str, instance):
    engineManager[name] = instance

# Register all engines
for EngineClass in [
    ARVEngine, AnalyticsEngine, CodeEngine, ConversationEngine, CreativityEngine,
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
