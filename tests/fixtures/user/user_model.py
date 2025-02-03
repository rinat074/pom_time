from pytest_factoryboy import register
from faker import Factory as FakerFactory
import factory
import pytest

from models import UserProfile

faker = FakerFactory.create()

@register(name="user_profile")
class UserProfileFactory(factory.Factory):
    class Meta:
        model = UserProfile

    id = factory.LazyFunction(faker.random_int)
    username = factory.LazyFunction(faker.user_name)
    password = factory.LazyFunction(faker.password)

@pytest.mark.asyncio
async def test_create_user_with_factory(user_service):
    user = UserProfileFactory(username="testuser", password="testpassword")
    
    user_login_data = await user_service.create_user(user.username, user.password)
    
    assert user_login_data.username == user.username