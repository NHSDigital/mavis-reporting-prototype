import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""

    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Flask config
    TEMPLATES_AUTO_RELOAD = True


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
