from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.schemas.auth_schema import LoginSchema
from app.services.auth_service import AuthService
from app.utils.exceptions import AuthenticationError
from app.models.auth import User
from app import db

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()
login_schema = LoginSchema()

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para autenticación de usuarios.
    La documentación de este endpoint está en /static/swagger.json
    """
    try:
        # Validar datos de entrada
        data = login_schema.load(request.get_json())

        # Autenticar usuario
        result = auth_service.authenticate(
            username=data['username'],
            password=data['password']
        )

        response = jsonify(result)
        return response, 200

    except ValidationError as e:
        return jsonify({'error': 'Datos de entrada inválidos', 'details': e.messages}), 400
    except AuthenticationError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/reset-admin-password', methods=['POST'])
def reset_admin_password():
    """Endpoint temporal para resetear la contraseña del admin."""
    try:
        user = User.query.filter_by(username='admin').first()
        if user:
            user.set_password('Admin123!')
            db.session.commit()
            return jsonify({'message': 'Contraseña actualizada'}), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500