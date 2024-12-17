from app import db
from .mixins import TimestampMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(TimestampMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    api_keys = db.relationship('ApiKey', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        print(f"Verificando contraseña. Hash almacenado: {self.password_hash}")
        result = check_password_hash(self.password_hash, password)
        print(f"Resultado de verificación: {result}")
        return result

    def __repr__(self):
        return f'<User {self.user_id}>'

class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    users = db.relationship('User', secondary='user_roles', back_populates='roles')

class UserRole(TimestampMixin, db.Model):
    __tablename__ = 'user_roles'

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), primary_key=True)
    role_id = db.Column(db.BigInteger, db.ForeignKey('roles.role_id'), primary_key=True)
    assigned_at = db.Column(db.DateTime, nullable=False)

class ApiKey(TimestampMixin, db.Model):
    __tablename__ = 'api_keys'

    api_key_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), nullable=False)
    key_value = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    expires_at = db.Column(db.DateTime)

    # Relaciones
    user = db.relationship('User', back_populates='api_keys')