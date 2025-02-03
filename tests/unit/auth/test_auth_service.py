import pytest
from jose import jwt
import datetime as dt
from dependency import get_auth_service
from service import AuthService
from settings import Settings
pytestmark = pytest.mark.asyncio

async def test_auth_service__success(auth_service):
    assert isinstance(auth_service, AuthService)


async def test_generate_access_token__success(auth_service, settings: Settings):
    access_token = auth_service.generate_access_token(user_id=1)
    decoded_token = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ENCODE_ALGORITHM)
    
    assert decoded_token["user_id"] == 1
    assert isinstance(access_token, str)
    assert decoded_token["exp"] > dt.datetime.now(dt.UTC).timestamp()

    
async def test_generate_user_id_from_token__success(auth_service, settings: Settings):
    access_token = auth_service.generate_access_token(user_id=1)
    user_id = auth_service.get_user_id_from_token(access_token)
    assert user_id == 1
