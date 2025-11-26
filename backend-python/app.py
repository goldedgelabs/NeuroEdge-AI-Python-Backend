# backend-python/app.py

from core.dbManager import db
from core.eventBus import eventBus
from core.engineManager import EngineManager
from core.agentManager import AgentManager
from db.replicationManager import replicateEdgeToShared
from utils.logger import logger

# -----------------------------
# Import all engines
# -----------------------------
from engines.AREngine import AREngine
from engines.AnalyticsEngine import AnalyticsEngine
from engines.CodeEngine import CodeEngine
from engines.ConversationEngine import ConversationEngine
from engines.CreativityEngine import CreativityEngine
from engines.CriticEngine import CriticEngine
from engines.DataIngestEngine import DataIngestEngine
from engines.DataInspectEngine import DataInspectEngine
from engines.DeviceProtectionEngine import DeviceProtectionEngine
from engines.DoctrineEngine import DoctrineEngine
from engines.EdgeDeviceEngine import EdgeDeviceEngine
from engines.GamingCreativeEngine import GamingCreativeEngine
from engines.GoldEdgeIntegrationEngine import GoldEdgeIntegrationEngine
from engines.HealthEngine import HealthEngine
from engines.MarketEngine import MarketEngine
from engines.MedicineManagementEngine import MedicineManagementEngine
from engines.MemoryEngine import MemoryEngine
from engines.MonitoringEngine import MonitoringEngine
from engines.MultiModalEngine import MultiModalEngine
from engines.OrchestrationEngine import OrchestrationEngine
from engines.PersonaEngine import PersonaEngine
from engines.PhoneSecurityEngine import PhoneSecurityEngine
from engines.PlannerEngine import PlannerEngine
from engines.PolicyEngine import PolicyEngine
from engines.PredictiveEngine import PredictiveEngine
from engines.RealTimeRecommenderEngine import RealTimeRecommenderEngine
from engines.ReasoningEngine import ReasoningEngine
from engines.RecommendationEngine import RecommendationEngine
from engines.ReinforcementEngine import ReinforcementEngine
from engines.ResearchAnalyticsEngine import ResearchAnalyticsEngine
from engines.ResearchEngine import ResearchEngine
from engines.SchedulerEngine import SchedulerEngine
from engines.SchedulingEngine import SchedulingEngine
from engines.SearchEngine import SearchEngine
from engines.SecurityEngine import SecurityEngine
from engines.SelfImprovementEngine import SelfImprovementEngine
from engines.SimulationEngine import SimulationEngine
from engines.SummarizationEngine import SummarizationEngine
from engines.TelemetryEngine import TelemetryEngine
from engines.TranslationEngine import TranslationEngine
from engines.VisionEngine import VisionEngine
from engines.VoiceEngine import VoiceEngine

# -----------------------------
# Import all agents
# -----------------------------
from agents.ARVAgent import ARVAgent
from agents.AnalyticsAgent import AnalyticsAgent
from agents.AntiTheftAgent import AntiTheftAgent
from agents.AutoUpdateAgent import AutoUpdateAgent
from agents.BackupAgent import BackupAgent
from agents.BillingAgent import BillingAgent
from agents.CollaborationAgent import CollaborationAgent
from agents.ComplianceAgent import ComplianceAgent
from agents.ContentModerationAgent import ContentModerationAgent
from agents.ConversationAgent import ConversationAgent
from agents.CorrectionAgent import CorrectionAgent
from agents.CreativityAgent import CreativityAgent
from agents.CriticAgent import CriticAgent
from agents.DataIngestAgent import DataIngestAgent
from agents.DataProcessingAgent import DataProcessingAgent
from agents.DecisionAgent import DecisionAgent
from agents.DeploymentAgent import DeploymentAgent
from agents.DeviceProtectionAgent import DeviceProtectionAgent
from agents.DiscoveryAgent import DiscoveryAgent
from agents.DistributedTaskAgent import DistributedTaskAgent
from agents.DoctrineAgent import DoctrineAgent
from agents.EncryptionAgent import EncryptionAgent
from agents.EvolutionAgent import EvolutionAgent
from agents.FeedbackAgent import FeedbackAgent
from agents.FounderAgent import FounderAgent
from agents.GPIAgent import GPIAgent
from agents.GlobalMedAgent import GlobalMedAgent
from agents.GoldEdgeIntegrationAgent import GoldEdgeIntegrationAgent
from agents.HealthMonitoringAgent import HealthMonitoringAgent
from agents.HotReloadAgent import HotReloadAgent
from agents.IdentityAgent import IdentityAgent
from agents.InspectionAgent import InspectionAgent
from agents.LearningAgent import LearningAgent
from agents.LoadBalancingAgent import LoadBalancingAgent
from agents.LocalStorageAgent import LocalStorageAgent
from agents.MarketAssessmentAgent import MarketAssessmentAgent
from agents.MetricsAgent import MetricsAgent
from agents.MonitoringAgent import MonitoringAgent
from agents.NotificationAgent import NotificationAgent
from agents.OfflineAgent import OfflineAgent
from agents.OrchestrationAgent import OrchestrationAgent
from agents.PersonalAgent import PersonalAgent
from agents.PhoneSecurityAgent import PhoneSecurityAgent
from agents.PlannerAgent import PlannerAgent
from agents.PlannerHelperAgent import PlannerHelperAgent
from agents.PluginManagerAgent import PluginManagerAgent
from agents.PredictionAgent import PredictionAgent
from agents.PredictiveAgent import PredictiveAgent
from agents.RecommendationAgent import RecommendationAgent
from agents.RecoveryAgent import RecoveryAgent
from agents.ResearchAgent import ResearchAgent
from agents.ResearchAnalyticsAgent import ResearchAnalyticsAgent
from agents.RoutingAgent import RoutingAgent
from agents.SchedulingAgent import SchedulingAgent
from agents.SearchAgent import SearchAgent
from agents.SecurityAgent import SecurityAgent
from agents.SecurityAuditAgent import SecurityAuditAgent
from agents.SelfHealingAgent import SelfHealingAgent
from agents.SelfImprovementAgent import SelfImprovementAgent
from agents.SelfProtectionAgent import SelfProtectionAgent
from agents.SimulationAgent import SimulationAgent
from agents.SummarizationAgent import SummarizationAgent
from agents.SupervisorAgent import SupervisorAgent
from agents.SyncAgent import SyncAgent
from agents.TelemetryAgent import TelemetryAgent
from agents.TestingAgent import TestingAgent
from agents.TranslationAgent import TranslationAgent
from agents.UIAgent import UIAgent
from agents.ValidationAgent import ValidationAgent
from agents.VerifierAgent import VerifierAgent
from agents.WorkerAgent import WorkerAgent

# -----------------------------
# Initialize Engines
# -----------------------------
engine_manager = EngineManager()
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
    instance = EngineClass()
    engine_manager.register_engine(EngineClass.__name__, instance)

# -----------------------------
# Initialize Agents
# -----------------------------
agent_manager = AgentManager()
for AgentClass in [
    ARVAgent, AnalyticsAgent, AntiTheftAgent, AutoUpdateAgent, BackupAgent,
    BillingAgent, CollaborationAgent, ComplianceAgent, ContentModerationAgent,
    ConversationAgent, CorrectionAgent, CreativityAgent, CriticAgent, DataIngestAgent,
    DataProcessingAgent, DecisionAgent, DeploymentAgent, DeviceProtectionAgent,
    DiscoveryAgent, DistributedTaskAgent, DoctrineAgent, EncryptionAgent, EvolutionAgent,
    FeedbackAgent, FounderAgent, GPIAgent, GlobalMedAgent, GoldEdgeIntegrationAgent,
    HealthMonitoringAgent, HotReloadAgent, IdentityAgent, InspectionAgent, LearningAgent,
    LoadBalancingAgent, LocalStorageAgent, MarketAssessmentAgent, MetricsAgent,
    MonitoringAgent, NotificationAgent, OfflineAgent, OrchestrationAgent, PersonalAgent,
    PhoneSecurityAgent, PlannerAgent, PlannerHelperAgent, PluginManagerAgent,
    PredictionAgent, PredictiveAgent, RecommendationAgent, RecoveryAgent, ResearchAgent,
    ResearchAnalyticsAgent, RoutingAgent, SchedulingAgent, SearchAgent, SecurityAgent,
    SecurityAuditAgent, SelfHealingAgent, SelfImprovementAgent, SelfProtectionAgent,
    SimulationAgent, SummarizationAgent, SupervisorAgent, SyncAgent, TelemetryAgent,
    TestingAgent, TranslationAgent, UIAgent, ValidationAgent, VerifierAgent, WorkerAgent
]:
    instance = AgentClass()
    agent_manager.register_agent(AgentClass.__name__, instance)

# -----------------------------
# Optional: replicate all edge data to shared on startup
# -----------------------------
async def replicate_all_on_startup():
    logger.log("[App] Replicating all edge data to shared...")
    await replicateEdgeToShared()
    logger.log("[App] Replication complete.")

# -----------------------------
# Main bootstrap
# -----------------------------
async def bootstrap():
    logger.log("[App] NeuroEdge Python backend starting...")
    await replicate_all_on_startup()
    logger.log("[App] All engines and agents are initialized and ready.")

# Run bootstrap if this file is executed directly
if __name__ == "__main__":
    import asyncio
    asyncio.run(bootstrap())
