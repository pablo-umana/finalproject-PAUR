from datetime import datetime, timedelta
import jwt
from flask import current_app
from app.models import User
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import AuthenticationError

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def authenticate(self, username: str, password: str) -> dict:
        """Autentica un usuario y genera un token JWT."""
        print(f"Intentando autenticar usuario: {username}")

        user = self.user_repository.find_by_username(username)
        print(f"Usuario encontrado en BD: {user}")

        if not user:
            raise AuthenticationError("Credenciales inválidas")

        # Verificar contraseña
        valid_password = user.check_password(password)
        print(f"Contraseña válida: {valid_password}")

        if not valid_password:
            raise AuthenticationError("Credenciales inválidas")

        if not user.is_active:
            raise AuthenticationError("Usuario inactivo")

        token = self._generate_token(user)
        print(f"Token generado: {token[:20]}...")

        return {
            'token': token,
            'user': {
                'id': user.user_id,
                'username': user.username,
                'email': user.email,
                'roles': [role.name for role in user.roles]
            }
        }

    def _generate_token(self, user: User) -> str:
        """Genera un token JWT para el usuario."""
        now = datetime.utcnow()
        payload = {
            'user_id': user.user_id,
            'username': user.username,
            'roles': [role.name for role in user.roles],
            'iat': now,
            'exp': now + timedelta(hours=24)
        }

        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )