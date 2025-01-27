from repository import UserRepository
from dataclasses import dataclass
from schema import UserLoginSchema

import random
import string

@dataclass
class UserService:

    user_repository: UserRepository
    
    def create_user(self, username: str, password: str) -> UserLoginSchema:
        access_token = self._generate_access_token()
        user = self.user_repository.create_user(username, password, access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _generate_access_token() -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


