from cryptography.fernet import Fernet
from pathlib import Path
from typing import Union
import os

CURRENT_APP_ENV = os.environ.get("ENV", "development")


class BaseConfig:
    DB_URL = os.environ["DB_URL"]

    TEMPLATE_DIR = str(Path(__file__).resolve().parent.joinpath("templates"))
    STATIC_DIR = str(Path(__file__).resolve().parent.joinpath("static"))
    UPLOAD_DIR = str(Path("/mnt/pemilos/").joinpath("uploads"))
    UPLOAD_URL = "/uploads"

    TEMPLATING_PATH_TO_TEMPLATES = TEMPLATE_DIR

    @classmethod
    def to_dict(cls):
        return {key: getattr(cls, key) for key in dir(cls) if key.isupper()}


class ProductionConfig(BaseConfig):
    SECRET_KEY = CURRENT_APP_ENV != "production" or os.environ["SECRET_KEY"]
    FORWARDED_SECRET = SECRET_KEY
    APP_ENV = "production"
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY", Fernet.generate_key())
    FORWARDED_SECRET = SECRET_KEY
    APP_ENV = "development"
    DEBUG = True


environ = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

current_env: Union[DevelopmentConfig, ProductionConfig] = environ[CURRENT_APP_ENV]
