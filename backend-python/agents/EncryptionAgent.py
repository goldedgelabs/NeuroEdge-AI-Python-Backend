from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import hashlib
import base64

class EncryptionAgent:
    name = "EncryptionAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def encrypt_data(self, data: dict):
        """
        Encrypts sensitive data using simple hashing for demonstration.
        """
        if not data:
            logger.warn(f"[EncryptionAgent] No data provided to encrypt")
            return None

        encrypted = {}
        for k, v in data.items():
            try:
                value_str = str(v)
                hashed = hashlib.sha256(value_str.encode("utf-8")).digest()
                encrypted[k] = base64.b64encode(hashed).decode("utf-8")
            except Exception as e:
                logger.error(f"[EncryptionAgent] Error encrypting key {k}: {e}")
                encrypted[k] = None

        # Save encrypted result to DB
        record_id = f"enc_{int(time.time()*1000)}"
        await db.set("encrypted_data", record_id, encrypted, target="edge")
        eventBus.publish("db:update", {"collection": "encrypted_data", "key": record_id, "value": encrypted, "source": self.name})

        logger.log(f"[EncryptionAgent] Data encrypted and saved: {record_id}")
        return {"id": record_id, "encrypted": encrypted}

    async def handle_db_update(self, event: dict):
        logger.log(f"[EncryptionAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[EncryptionAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[EncryptionAgent] Recovering from error: {error}")
