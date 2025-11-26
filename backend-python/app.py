# backend-python/app.py
import asyncio
from core.dbManager import db
from core.engineManager import engineManager
from core.agentManager import agentManager
from db.replicationManager import replicateEdgeToShared
from utils.logger import logger

# -----------------------------
# Optional: replicate all edge data to shared
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
    logger.log("[App] All engines and agents initialized and ready.")

    # Optional: sample execution
    if "AnalyticsEngine" in engineManager:
        result = await engineManager["AnalyticsEngine"].run({"folder": "test", "role": "user"})
        logger.log(f"[App] Sample AnalyticsEngine output: {result}")

    if "ResearchAgent" in agentManager:
        research_result = await agentManager["ResearchAgent"].conduct_research("COVID", {"data": [1,2,3,4,5]})
        logger.log(f"[App] Sample ResearchAgent output: {research_result}")

    all_research = await db.get_all("research_results")
    logger.log(f"[App] All research_results in DB: {all_research}")

# -----------------------------
# Run bootstrap
# -----------------------------
if __name__ == "__main__":
    asyncio.run(bootstrap())
