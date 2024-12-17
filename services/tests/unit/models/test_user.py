import pytest
from app.models.auth import User
from werkzeug.security import generate_password_hash

class TestUser:
    def test_set_password_creates_hash(self):
        """Test que la contraseña se convierte correctamente a hash."""
        user = User()
        password = "test_password123"

        user.set_password(password)

        assert user.password_hash is not None
        assert user.password_hash != password
        assert user.password_hash.startswith('pbkdf2:sha256')

    def test_verify_correct_password(self):
        """Test que una contraseña correcta se valida exitosamente."""
        user = User()
        password = "test_password123"
        user.set_password(password)

        assert user.check_password(password) is True

    def test_verify_incorrect_password(self):
        """Test que una contraseña incorrecta falla la validación."""
        user = User()
        password = "test_password123"
        user.set_password(password)

        assert user.check_password("wrong_password") is False

    def test_passwords_are_random(self):
        """Test que el mismo password genera diferentes hashes."""
        user1 = User()
        user2 = User()
        password = "test_password123"

        user1.set_password(password)
        user2.set_password(password)

        assert user1.password_hash != user2.password_hash