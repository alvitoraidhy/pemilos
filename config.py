import os

class BaseConfig:
    APP_PORT = os.environ.get('PORT', 8000)
    APP_HOST = os.environ.get('HOST', '0.0.0.0')

class ProductionConfig(BaseConfig):
    APP_ENV = 'production'
    DB_URL = os.environ.get('DB_URL')

class DevelopmentConfig(BaseConfig):
    APP_ENV = 'development'
    DB_URL = 'sqlite://.//development.db'

classes = {
    'production': ProductionConfig,
    'development': DevelopmentConfig
}