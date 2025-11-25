import logging
import sys

# Configure global logger
logger = logging.getLogger("NeuroEdge")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

def log(msg: str):
    logger.info(msg)

def warn(msg: str):
    logger.warning(msg)

def error(msg: str):
    logger.error(msg)
