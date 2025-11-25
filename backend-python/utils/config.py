import os

# Environment
ENV = os.getenv("NEUROEDGE_ENV", "development")

# Database paths
LOCAL_DB_PATH = os.getenv("LOCAL_DB_PATH", "./database/local")
DISTRIBUTED_DB_URL = os.getenv("DISTRIBUTED_DB_URL", "http://localhost:8000")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# System constants
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
EVENT_LOOP_INTERVAL = float(os.getenv("EVENT_LOOP_INTERVAL", "0.1"))
