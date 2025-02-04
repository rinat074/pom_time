from dataclasses import dataclass, field
import pytest

@dataclass
class FakeUserRepository:
    _users: dict = field(default_factory=dict)

    async def create_user(self, username: str, password: str):
        # Простой генератор идентификатора пользователя
        user_id = len(self._users) + 1
        # Создаем объект пользователя (можно использовать простой объект)
        user = type("User", (), {"id": user_id, "username": username, "password": password})
        self._users[username] = user
        return user

    async def get_user_by_username(self, username: str):
        return self._users.get(username, None)

@pytest.fixture
def fake_user_repository():
    return FakeUserRepository()