from flask import jsonify, request
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Manejar excepciones HTTP y retornar JSON."""
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }).data
        response.content_type = "application/json"
        return response

    @app.after_request
    def after_request(response):
        """Asegurar headers CORS en todas las respuestas."""
        origin = request.headers.get('Origin', '*')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers',
                           'Content-Type, Authorization, Access-Control-Allow-Credentials')
        response.headers.add('Access-Control-Allow-Methods',
                           'GET, POST, PUT, DELETE, OPTIONS')

        # Manejar preflight requests
        if request.method == 'OPTIONS':
            response.status_code = 200

        return response