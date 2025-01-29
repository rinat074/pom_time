from schema import UserLoginSchema
from dataclasses import dataclass
from repository import UserRepository
from exception import TokenExpiredError, TokenNotValidError, UserNotFoundError, UserPasswordError
from models import UserProfile
from jose import JWTError, jwt
from datetime import datetime, timedelta

from settings import settings

@dataclass
class AuthService:

    user_repository: UserRepository

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_user(user, password)
        access_token = self.generate_access_token(user_id = user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_user(user: UserProfile, password: str):
        if user is None:
            raise UserNotFoundError
        if user.password != password:
            raise UserPasswordError

    def logout(self, access_token: str) -> None:
        pass

    def generate_access_token(self, user_id: int) -> str:
        expire_date = (datetime.utcnow() + timedelta(days=10)).timestamp()
        to_encode = {"user_id": user_id, "exp": expire_date}
        try:
            token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ENCODE_ALGORITHM)
        except Exception as e:
            print(f"Error generating access token: {e}")
        return token

    def get_user_id_from_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ENCODE_ALGORITHM])
            if payload['expired'] < datetime.utcnow().timestamp():
                raise TokenExpiredError
            return payload.get("user_id")
        except JWTError as e:
            print(f"Error getting user id from token: {e}")
            raise TokenNotValidError
