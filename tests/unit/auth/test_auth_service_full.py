import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException

from service.auth import AuthService
from exception import UserNotFoundError, UserPasswordError
from settings import settings

# Определяем класс-имитацию пользователя
class DummyUser:
    def __init__(self, user_id: int, username: str, password: str):
        self.id = user_id
        self.username = username
        self.password = password

# Фейковый репозиторий для успешного случая входа
class DummyUserRepositorySuccess:
    async def get_user_by_username(self, username: str):
        if username == "test":
            return DummyUser(user_id=1, username="test", password="secret")
        return None

# Фейковый репозиторий, который всегда не находит пользователя
class DummyUserRepositoryNotFound:
    async def get_user_by_username(self, username: str):
        return None

# Фейковый репозиторий, возвращающий пользователя с корректным паролем,
# что позволяет проверить случай неверного пароля при аутентификации
class DummyUserRepositoryInvalidPassword:
    async def get_user_by_username(self, username: str):
        # Возвращаем пользователя с паролем "secret" независимо от запроса
        return DummyUser(user_id=1, username="test", password="secret")

@pytest.mark.asyncio
async def test_login_success():
    """
    Тест успешного входа: пользователь найден и пароль совпадает.
    Проверяем, что возвращается корректный токен, из которого возможно извлечь верный user_id.
    """
    dummy_repo = DummyUserRepositorySuccess()
    auth_service = AuthService(user_repository=dummy_repo)
    
    login_data = await auth_service.login("test", "secret")
    decoded_token = jwt.decode(
        login_data.access_token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ENCODE_ALGORITHM]
    )
    assert login_data.user_id == 1
    assert decoded_token["user_id"] == 1

@pytest.mark.asyncio
async def test_login_user_not_found():
    """
    Тестирование ситуации, когда пользователь не найден.
    Ожидается выброс исключения UserNotFoundError.
    """
    dummy_repo = DummyUserRepositoryNotFound()
    auth_service = AuthService(user_repository=dummy_repo)
    
    with pytest.raises(UserNotFoundError):
        await auth_service.login("nonexistent", "any")

@pytest.mark.asyncio
async def test_login_invalid_password():
    """
    Тестирование ситуации, когда пароль неверный.
    Ожидается выброс исключения UserPasswordError.
    """
    dummy_repo = DummyUserRepositoryInvalidPassword()
    auth_service = AuthService(user_repository=dummy_repo)
    
    with pytest.raises(UserPasswordError):
        await auth_service.login("test", "wrongpassword")

@pytest.mark.asyncio
async def test_generate_access_token_is_string(auth_service):
    """
    Проверка, что метод generate_access_token возвращает строку.
    """
    token = auth_service.generate_access_token(user_id=1)
    assert isinstance(token, str)

def test_get_user_id_from_token_success(auth_service, settings):
    """
    Проверяем, что из корректного токена успешно извлекается user_id.
    """
    access_token = auth_service.generate_access_token(user_id=1)
    user_id = auth_service.get_user_id_from_token(access_token)
    assert user_id == 1

def test_get_user_id_from_token_expired(auth_service, settings):
    """
    Тест для случая, когда токен просрочен.
    Формируем токен с временем истечения в прошлом и проверяем, что метод
    get_user_id_from_token выбрасывает HTTPException с деталями "Token has expired".
    """
    expired_payload = {
        "user_id": 1,
        "exp": (datetime.now(timezone.utc) - timedelta(minutes=5)).timestamp()
    }
    expired_token = jwt.encode(
        expired_payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ENCODE_ALGORITHM
    )
    with pytest.raises(HTTPException) as exc_info:
        auth_service.get_user_id_from_token(expired_token)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token has expired"

def test_get_user_id_from_token_invalid(auth_service):
    """
    Тест для проверки ситуации с некорректным токеном.
    Передаем явно неверное значение, ожидая выброс исключения с деталями "Invalid token".
    """
    invalid_token = "invalid.token.value"
    with pytest.raises(HTTPException) as exc_info:
        auth_service.get_user_id_from_token(invalid_token)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"