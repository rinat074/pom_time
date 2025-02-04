import uuid
import pytest
from jose import jwt
from service.auth import AuthService
from exception import UserNotFoundError, UserPasswordError
from settings import settings

@pytest.mark.asyncio
async def test_login_success(db_session, user_repository):
    # Создаём уникального пользователя в базе
    unique_username = f"testlogin_{uuid.uuid4().hex}"
    password = "secret"
    created_user = await user_repository.create_user(unique_username, password)
    
    auth_service = AuthService(user_repository=user_repository)
    
    # Проводим аутентификацию
    login_data = await auth_service.login(unique_username, password)
    
    # Декодируем токен и проверяем, что user_id совпадает
    decoded_token = jwt.decode(
        login_data.access_token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ENCODE_ALGORITHM]
    )
    assert login_data.user_id == created_user.id
    assert decoded_token["user_id"] == created_user.id

@pytest.mark.asyncio
async def test_login_user_not_found(db_session, user_repository):
    auth_service = AuthService(user_repository=user_repository)
    
    non_existent_username = "nonexistent_" + uuid.uuid4().hex
    with pytest.raises(UserNotFoundError):
        await auth_service.login(non_existent_username, "any_password")

@pytest.mark.asyncio
async def test_login_invalid_password(db_session, user_repository):
    # Создаём пользователя с известным паролем
    unique_username = f"testlogin_invalid_{uuid.uuid4().hex}"
    correct_password = "correctpass"
    await user_repository.create_user(unique_username, correct_password)
    
    auth_service = AuthService(user_repository=user_repository)
    
    # Пытаемся залогиниться с неверным паролем
    with pytest.raises(UserPasswordError):
        await auth_service.login(unique_username, "wrongpass")