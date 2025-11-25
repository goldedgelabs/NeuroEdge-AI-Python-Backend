# NotificationAgent.py
# Agent responsible for sending notifications via multiple channels (email, SMS, push)

class NotificationAgent:
    def __init__(self):
        self.name = "NotificationAgent"

    async def send_notification(self, message: str, channels: list = None, user_id: str = None):
        """
        Send notification to user or system via specified channels.
        channels: ["email", "sms", "push"]
        """
        if channels is None:
            channels = ["email"]  # default channel

        results = {}
        for channel in channels:
            # Stub: simulate sending notification
            results[channel] = f"Sent to {user_id or 'system'} via {channel}: {message}"
            print(results[channel])

        return results

    async def handleDBUpdate(self, data):
        """
        React to DB updates if notification is needed
        """
        print(f"[NotificationAgent] DB Update received: {data}")

    async def recover(self, error):
        print(f"[NotificationAgent] Recovered from error: {error}")
