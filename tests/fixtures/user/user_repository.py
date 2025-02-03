from dataclasses import dataclass
import pytest

@dataclass
class FakeUserRepository:
    ...

@pytest.fixture
def user_repository():
    return FakeUserRepository()
