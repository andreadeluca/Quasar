from dotenv import load_dotenv, find_dotenv
import os
from logging import getLogger

logger = getLogger(__name__)

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            instance = super().__new__(cls)
            env_path = find_dotenv()
            if load_dotenv(env_path):
                logger.info(f"Loaded environment from {env_path}")
            else:
                logger.warning("No .env file found, using system environment only")
            cls._instance = instance
        return cls._instance

    def get(self, key, default=None):
        value = os.getenv(key, default)
        if value is None:
            logger.warning(f"Missing env var: {key}")
        return value

settings = ConfigManager()
