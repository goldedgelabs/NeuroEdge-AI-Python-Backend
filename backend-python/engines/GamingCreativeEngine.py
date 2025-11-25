from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class GamingCreativeEngine:
    name = "GamingCreativeEngine"

    def __init__(self):
        self.projects = {}

    async def create_project(self, project_id, data):
        self.projects[project_id] = data
        # Write to DB and emit event
        await db.set("gaming_projects", project_id, data, storage="edge")
        eventBus.publish("db:update", {
            "collection": "gaming_projects",
            "key": project_id,
            "value": data,
            "source": self.name
        })
        log(f"[{self.name}] Project created: {project_id}")
        return {"success": True, "project_id": project_id}

    async def update_project(self, project_id, data):
        if project_id in self.projects:
            self.projects[project_id].update(data)
            await db.set("gaming_projects", project_id, self.projects[project_id], storage="edge")
            eventBus.publish("db:update", {
                "collection": "gaming_projects",
                "key": project_id,
                "value": self.projects[project_id],
                "source": self.name
            })
            log(f"[{self.name}] Project updated: {project_id}")
            return {"success": True}
        return {"success": False, "message": "Project not found"}

    async def delete_project(self, project_id):
        if project_id in self.projects:
            del self.projects[project_id]
            await db.delete("gaming_projects", project_id)
            eventBus.publish("db:delete", {"collection": "gaming_projects", "key": project_id, "source": self.name})
            log(f"[{self.name}] Project deleted: {project_id}")
            return {"success": True}
        return {"success": False, "message": "Project not found"}

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
