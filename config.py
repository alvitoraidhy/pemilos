from cryptography.fernet import Fernet
import os

class BaseConfig:
    APP_PORT = os.environ.get('PORT', 8000)
    APP_HOST = os.environ.get('HOST', '0.0.0.0')
    SECRET_KEY = os.environ.get('SECRET_KEY')  or Fernet.generate_key()

class ProductionConfig(BaseConfig):
    APP_ENV = 'production'
    DB_URL = os.environ.get('DB_URL')
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    APP_ENV = 'development'
    DEBUG = True
    DB_URL = 'sqlite://.//development.db'

classes = {
    'production': ProductionConfig,
    'development': DevelopmentConfig
}
