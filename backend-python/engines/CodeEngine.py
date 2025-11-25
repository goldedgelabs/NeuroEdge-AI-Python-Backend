from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus

class CodeEngine(EngineBase):
    async def run(self, input_data):
        """
        Executes code snippets or scripts from input_data.
        """
        code_snippet = input_data.get("code", "")
        # WARNING: In production, use a safe sandbox for code execution
        try:
            exec_locals = {}
            exec(code_snippet, {}, exec_locals)
            result_value = exec_locals.get("result", "No result returned")
        except Exception as e:
            result_value = f"Execution error: {e}"

        result = {
            "collection": "code_executions",
            "id": input_data.get("id", "default_code"),
            "input": code_snippet,
            "result": result_value
        }

        await db.set(result["collection"], result["id"], result, "edge")
        await event_bus.publish("db:update", result)
        return result
