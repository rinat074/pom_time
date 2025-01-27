from schema import UserLoginSchema
from dataclasses import dataclass
from repository import UserRepository
from exception import UserNotFoundError, UserPasswordError
from models import UserProfile

@dataclass
class AuthService:

    user_repository: UserRepository
    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_user(user, password)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _validate_user(user: UserProfile, password: str):
        if user is None:
            raise UserNotFoundError
        if user.password != password:
            raise UserPasswordError

    def logout(self, access_token: str) -> None:
        pass
