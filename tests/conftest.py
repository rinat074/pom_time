import asyncio
import pytest
from models import Base, UserProfile, Tasks, Categories

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

pytest_plugins = [
    "tests.fixtures.database",
    "tests.fixtures.auth.clients",
    "tests.fixtures.auth.auth_service",
    "tests.fixtures.user.user_repository",
    "tests.fixtures.settings",
    "tests.fixtures.user.user_model",
    "tests.fixtures.common"
]
