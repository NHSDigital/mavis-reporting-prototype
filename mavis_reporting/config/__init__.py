import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    # Used as the base for constructing URLs to
    # exchange auth tokens, and request data
    MAVIS_ROOT_URL = os.environ.get("MAVIS_ROOT_URL") or "http://localhost:4000/"

    # Flask config
    TEMPLATES_AUTO_RELOAD = True
    SESSION_TTL_SECONDS = int(os.environ.get("SESSION_TTL_SECONDS") or "600")

    # If this is set to True, you will always have a session as user_id 1,
    # nurse.joy@example.com, org: R1L, role: S8000:G8000:R8001
    # (the default user from db/seeds.rb on the main mavis app)
    FAKE_LOGIN_ENABLED = bool(os.environ.get("FAKE_LOGIN_ENABLED"))


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    TESTING = False
    LOG_LEVEL = "DEBUG"
    # Uncomment this line to allow developing locally without having
    # the main Mavis running:
    # FAKE_LOGIN_ENABLED = True


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
