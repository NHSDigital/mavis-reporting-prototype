import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    # Used as the base for constructing URLs to
    # exchange auth tokens, and request data
    MAVIS_ROOT_URL = os.environ.get("MAVIS_ROOT_URL")

    # Flask config
    TEMPLATES_AUTO_RELOAD = True
    SESSION_TTL_SECONDS = int(os.environ.get("SESSION_TTL_SECONDS") or "600")


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    TESTING = False
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    TESTING = False
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
