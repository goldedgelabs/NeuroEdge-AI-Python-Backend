# backend-python/api.py
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from core.engineManager import engineManager
from core.agentManager import agentManager
from core.dbManager import db
from core.eventBus import eventBus
from db.replicationManager import replicateEdgeToShared
from utils.logger import logger

app = FastAPI(title="NeuroEdge Python Backend API")

# Allow CORS for frontend / other backends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# REST Endpoints
# -----------------------------

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/db/{collection}")
async def get_collection(collection: str):
    data = await db.get_all(collection)
    return {"collection": collection, "data": data}

@app.get("/db/{collection}/{key}")
async def get_record(collection: str, key: str):
    record = await db.get(collection, key)
    return {"collection": collection, "key": key, "record": record}

@app.post("/engine/{engine_name}/run")
async def run_engine(engine_name: str, payload: dict):
    engine = engineManager.get(engine_name)
    if not engine:
        return {"error": f"Engine {engine_name} not found"}
    result = await engine.run(payload)
    return {"engine": engine_name, "result": result}

@app.post("/agent/{agent_name}/task")
async def run_agent(agent_name: str, task: dict):
    agent = agentManager.get(agent_name)
    if not agent:
        return {"error": f"Agent {agent_name} not found"}
    if hasattr(agent, "handle"):
        result = await agent.handle(task)
        return {"agent": agent_name, "result": result}
    return {"error": f"Agent {agent_name} cannot handle tasks"}

# -----------------------------
# WebSocket for live events
# -----------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.log("[WebSocket] Client connected")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.log("[WebSocket] Client disconnected")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

ws_manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Optional: handle client commands
            await websocket.send_json({"received": data})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

# -----------------------------
# EventBus → WebSocket bridge
# -----------------------------
async def broadcast_db_update(event: dict):
    await ws_manager.broadcast({"type": "db_update", "payload": event})

eventBus.subscribe("db:update", broadcast_db_update)
eventBus.subscribe("db:delete", broadcast_db_update)

# -----------------------------
# Startup tasks
# -----------------------------
@app.on_event("startup")
async def startup_event():
    logger.log("[API] Startup: replicating edge → shared")
    await replicateEdgeToShared()
    logger.log("[API] Startup complete")
