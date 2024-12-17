from typing import Optional
from app.models import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def find_by_username(self, username: str) -> Optional[User]:
        """Busca un usuario por su nombre de usuario."""
        return User.query.filter_by(username=username).first()

    def find_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su email."""
        return User.query.filter_by(email=email).first()