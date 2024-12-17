from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os
from .config import config

# Inicialización de extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configuración simplificada de CORS
    CORS(app,
         resources={r"/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Configuración de Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'

    swagger_config = {
        'app_name': "API de Generación de PDFs",
        'swagger_ui_bundle_js': '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js',
        'swagger_ui_standalone_preset_js': '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js',
        'swagger_ui_css': '//unpkg.com/swagger-ui-dist@3/swagger-ui.css',
        'swagger_ui_version': '3',
    }

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config=swagger_config
    )

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    from .api.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Registrar manejadores de errores
    from .utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    return app