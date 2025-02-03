import pytest
from schema import UserLoginSchema
from tests.fixtures.user.user_model import UserProfileFactory
from tests.fixtures.common import db_session, user_repository, auth_service, user_service  # импортируем фикстуры

@pytest.mark.asyncio
async def test_create_user(user_service):
    username = "testuser"
    password = "testpassword"
    
    user_login_data = await user_service.create_user(username, password)
    
    assert user_login_data.user_id is not None
    assert isinstance(user_login_data.access_token, str)