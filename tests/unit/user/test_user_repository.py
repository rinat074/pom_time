import uuid
import pytest
from repository.user import UserRepository
from tests.fixtures.database import db_session

@pytest.mark.asyncio
async def test_create_and_get_user(db_session, user_repository: UserRepository):
    # Генерируем уникальное имя пользователя для теста
    unique_username = f"testuser_{uuid.uuid4().hex}"
    password = "testpassword"
    
    # Создаём пользователя через репозиторий
    created_user = await user_repository.create_user(unique_username, password)
    
    # Проверяем, что пользователь создан и данные корректны
    assert created_user is not None
    assert created_user.username == unique_username

    # Пытаемся получить пользователя по имени
    fetched_user = await user_repository.get_user_by_username(unique_username)
    
    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.username == unique_username

@pytest.mark.asyncio
async def test_get_user_by_username_not_found(user_repository: UserRepository):
    # Ищем пользователя с несуществующим именем
    non_existent_username = "nonexistent_" + uuid.uuid4().hex
    user = await user_repository.get_user_by_username(non_existent_username)
    
    assert user is None