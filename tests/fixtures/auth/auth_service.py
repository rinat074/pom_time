from service import AuthService
import pytest

@pytest.fixture
def auth_service(user_repository):
    return AuthService(user_repository=user_repository)

