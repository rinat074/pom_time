from settings import Settings

import pytest


@pytest.fixture
def settings():
    return Settings()

