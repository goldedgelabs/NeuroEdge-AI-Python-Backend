# LoadBalancingAgent.py
# Agent responsible for distributing workload evenly across available nodes or services

class LoadBalancingAgent:
    def __init__(self):
        self.name = "LoadBalancingAgent"
        self.nodes = []

    def register_node(self, node_id: str):
        if node_id not in self.nodes:
            self.nodes.append(node_id)
            print(f"[LoadBalancingAgent] Node registered: {node_id}")

    def unregister_node(self, node_id: str):
        if node_id in self.nodes:
            self.nodes.remove(node_id)
            print(f"[LoadBalancingAgent] Node unregistered: {node_id}")

    async def balance(self, task: dict):
        """
        Distribute task to a node using round-robin or other strategy
        """
        if not self.nodes:
            print("[LoadBalancingAgent] No nodes available to balance task")
            return {"status": "failed", "reason": "no nodes"}
        
        node = self.nodes[0]
        # Simple rotation
        self.nodes = self.nodes[1:] + [node]
        print(f"[LoadBalancingAgent] Task assigned to node: {node}")
        return {"status": "success", "node": node, "task": task}

    async def recover(self, error):
        print(f"[LoadBalancingAgent] Recovered from error: {error}")
