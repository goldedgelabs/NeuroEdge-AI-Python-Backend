from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class SimulationEngine:
    name = "SimulationEngine"

    def __init__(self):
        self.simulations = {}

    async def create_simulation(self, sim_id: str, config: dict):
        """Create a new simulation."""
        self.simulations[sim_id] = config

        # Save to DB and emit update
        await db.set("simulations", sim_id, config, storage="edge")
        eventBus.publish("db:update", {
            "collection": "simulations",
            "key": sim_id,
            "value": config,
            "source": self.name
        })
        log(f"[{self.name}] Simulation created: {sim_id}")
        return config

    async def run_simulation(self, sim_id: str, input_data: dict):
        """Run simulation and return results (mocked)."""
        config = self.simulations.get(sim_id)
        if not config:
            log(f"[{self.name}] Simulation not found: {sim_id}")
            return {"error": "Simulation not found"}

        # Here you can implement actual simulation logic
        result = {"sim_id": sim_id, "input": input_data, "result": "success"}
        
        # Save result to DB and emit update
        await db.set("simulation_results", sim_id, result, storage="edge")
        eventBus.publish("db:update", {
            "collection": "simulation_results",
            "key": sim_id,
            "value": result,
            "source": self.name
        })
        log(f"[{self.name}] Simulation run complete: {sim_id}")
        return result

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
