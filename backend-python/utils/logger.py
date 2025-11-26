# backend-python/utils/logger.py
import time

class Logger:
    def log(self, msg: str):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] INFO: {msg}")

    def warn(self, msg: str):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] WARN: {msg}")

    def error(self, msg: str):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {msg}")

logger = Logger()
