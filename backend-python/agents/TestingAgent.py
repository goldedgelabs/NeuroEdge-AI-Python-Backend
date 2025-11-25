# TestingAgent.py
# Agent responsible for automated testing and validation of system components

class TestingAgent:
    def __init__(self):
        self.name = "TestingAgent"
        self.test_results = []
        print("[TestingAgent] Initialized")

    def run_unit_test(self, test_name: str, test_func):
        try:
            result = test_func()
            status = "passed" if result else "failed"
            self.test_results.append({"test": test_name, "status": status})
            print(f"[TestingAgent] Unit test '{test_name}' {status}")
            return {"test": test_name, "status": status}
        except Exception as e:
            self.test_results.append({"test": test_name, "status": "error", "error": str(e)})
            print(f"[TestingAgent] Unit test '{test_name}' error: {e}")
            return {"test": test_name, "status": "error", "error": str(e)}

    def get_test_summary(self):
        summary = {
            "total_tests": len(self.test_results),
            "passed": sum(1 for r in self.test_results if r["status"] == "passed"),
            "failed": sum(1 for r in self.test_results if r["status"] == "failed"),
            "errors": sum(1 for r in self.test_results if r["status"] == "error"),
        }
        print(f"[TestingAgent] Test summary: {summary}")
        return summary

    async def handle_test_request(self, request: dict):
        action = request.get("action")
        if action == "run_unit_test":
            test_name = request.get("test_name")
            test_func = request.get("test_func")
            return self.run_unit_test(test_name, test_func)
        elif action == "get_summary":
            return self.get_test_summary()
        else:
            return {"error": "Invalid action"}

    async def recover(self, error):
        print(f"[TestingAgent] Recovered from error: {error}")
