import os
from dotenv import load_dotenv

# Cargar .env solo en desarrollo
if os.getenv('FLASK_ENV') != 'production':
    load_dotenv()

class Config:
    # Configuración base
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-12345')

    # Configuración de base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # Opciones del motor de base de datos
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,  # Tamaño del pool de conexiones
        'max_overflow': 20,  # Conexiones adicionales permitidas
        'pool_timeout': 30,  # Timeout para obtener una conexión
        'pool_recycle': 1800,  # Reciclar conexiones cada 30 minutos
    }

    # Otras opciones de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('FLASK_ENV') == 'development'  # SQL logging en desarrollo

    # Configuración de CORS
    CORS_HEADERS = 'Content-Type'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Mostrar SQL queries
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_timeout': 10,
    }

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'max_overflow': 40,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/templates_test')

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}