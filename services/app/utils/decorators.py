from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.models import User
from app.utils.exceptions import AuthenticationError, AuthorizationError

def jwt_required(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Permitir acceso sin token para rutas públicas
            if request.endpoint and 'login' in request.endpoint:
                return f(*args, **kwargs)

            token = None

            # Obtener token del header
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    raise AuthenticationError('Token inválido')

            if not token:
                raise AuthenticationError('Token no proporcionado')

            try:
                # Decodificar token
                payload = jwt.decode(
                    token,
                    current_app.config['SECRET_KEY'],
                    algorithms=['HS256']
                )

                # Verificar roles si se especificaron
                if roles:
                    user_roles = set(payload.get('roles', []))
                    required_roles = set(roles if isinstance(roles, list) else [roles])
                    if not required_roles.intersection(user_roles):
                        raise AuthorizationError('No tiene los permisos necesarios')

                return f(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                raise AuthenticationError('Token expirado')
            except jwt.InvalidTokenError:
                raise AuthenticationError('Token inválido')

        return decorated_function
    return decorator