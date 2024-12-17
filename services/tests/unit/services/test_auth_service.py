import pytest
from app.services.auth_service import AuthService
from app.models.auth import User
from app.utils.exceptions import AuthenticationError

class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        return AuthService()

    @pytest.fixture
    def mock_user(self, mocker):
        user = User()
        user.user_id = 1
        user.username = "test_user"
        user.email = "test@example.com"
        user.is_active = True
        user.set_password("correct_password")
        user.roles = []
        return user

    def test_authenticate_success(self, auth_service, mock_user, mocker):
        """Test autenticación exitosa con credenciales correctas."""
        # Mock del repositorio
        mocker.patch.object(
            auth_service.user_repository,
            'find_by_username',
            return_value=mock_user
        )

        result = auth_service.authenticate("test_user", "correct_password")

        assert result['token'] is not None
        assert result['user']['username'] == "test_user"
        assert result['user']['email'] == "test@example.com"

    def test_authenticate_invalid_username(self, auth_service, mocker):
        """Test que falla con usuario inexistente."""
        mocker.patch.object(
            auth_service.user_repository,
            'find_by_username',
            return_value=None
        )

        with pytest.raises(AuthenticationError) as exc:
            auth_service.authenticate("wrong_user", "any_password")

        assert str(exc.value) == "Credenciales inválidas"

    def test_authenticate_invalid_password(self, auth_service, mock_user, mocker):
        """Test que falla con contraseña incorrecta."""
        mocker.patch.object(
            auth_service.user_repository,
            'find_by_username',
            return_value=mock_user
        )

        with pytest.raises(AuthenticationError) as exc:
            auth_service.authenticate("test_user", "wrong_password")

        assert str(exc.value) == "Credenciales inválidas"

    def test_authenticate_inactive_user(self, auth_service, mock_user, mocker):
        """Test que falla con usuario inactivo."""
        mock_user.is_active = False
        mocker.patch.object(
            auth_service.user_repository,
            'find_by_username',
            return_value=mock_user
        )

        with pytest.raises(AuthenticationError) as exc:
            auth_service.authenticate("test_user", "correct_password")

        assert str(exc.value) == "Usuario inactivo"

    def test_token_contains_required_fields(self, auth_service, mock_user, mocker):
        """Test que el token contiene todos los campos necesarios."""
        mocker.patch.object(
            auth_service.user_repository,
            'find_by_username',
            return_value=mock_user
        )

        result = auth_service.authenticate("test_user", "correct_password")

        assert 'token' in result
        assert 'user' in result
        assert 'id' in result['user']
        assert 'username' in result['user']
        assert 'email' in result['user']
        assert 'roles' in result['user']