# BackupAgent.py
# Agent responsible for backing up data to local or remote storage

class BackupAgent:
    def __init__(self):
        self.name = "BackupAgent"

    async def perform_backup(self, collection: str = None):
        """
        Perform backup of specific collection or entire database if collection is None
        """
        if collection:
            print(f"[BackupAgent] Backing up collection: {collection}")
        else:
            print("[BackupAgent] Backing up entire database")
        # Simulate backup operation
        return {"status": "success", "collection": collection or "all"}

    async def handleDBUpdate(self, data):
        """
        Optional: react to DB changes if incremental backup is needed
        """
        print(f"[BackupAgent] DB Update received: {data}")

    async def recover(self, error):
        print(f"[BackupAgent] Recovered from error: {error}")
