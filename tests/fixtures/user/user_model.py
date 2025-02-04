from pytest_factoryboy import register
from faker import Factory as FakerFactory
import factory

from models import UserProfile

faker = FakerFactory.create()

@register(name="user_profile")
class UserProfileFactory(factory.Factory):
    class Meta:
        model = UserProfile

    id = factory.LazyFunction(faker.random_int)
    username = factory.LazyFunction(faker.user_name)
    password = factory.LazyFunction(faker.password)
