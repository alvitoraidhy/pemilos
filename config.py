from cryptography.fernet import Fernet
from pathlib import Path
import os

class BaseConfig:
    APP_PORT = os.environ.get('PORT', 8000)
    APP_HOST = os.environ.get('HOST', '0.0.0.0')
    APP_CONFIG_FILE = str(Path(__file__).resolve().parent.joinpath('app_config.ini'))
    SECRET_KEY = os.environ.get('SECRET_KEY') or Fernet.generate_key()
    FORWARDED_SECRET = SECRET_KEY
    WORKERS = int(os.environ.get('WORKERS', 1))

    @classmethod
    def to_dict(cls):
        return {key: getattr(cls, key) for key in dir(cls) if key.isupper()}

class ProductionConfig(BaseConfig):
    APP_ENV = 'production'
    DEBUG = False
    DB_URL = os.environ.get('DB_URL')
    STATIC_DIR = str(Path(__file__).resolve().parent.joinpath('static'))
    UPLOAD_DIR = str(Path(__file__).resolve().parent.joinpath('uploads'))
    UPLOAD_URL = '/uploads'


class DevelopmentConfig(BaseConfig):
    APP_ENV = 'development'
    DEBUG = True
    DB_URL = os.environ.get('DB_URL', 'sqlite://.//development.db')
    STATIC_DIR = str(Path(__file__).resolve().parent.joinpath('static'))
    UPLOAD_DIR = str(Path(__file__).resolve().parent.joinpath('uploads-dev'))
    UPLOAD_URL = '/uploads'

classes = {
    'production': ProductionConfig,
    'development': DevelopmentConfig
}
