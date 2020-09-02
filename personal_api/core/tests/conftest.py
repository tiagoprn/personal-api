# Here go your pytest fixtures, that can be used on your tests.

import pytest


@pytest.fixture
def content_payload():
    return {"name": "Hal Jordan", "complexity": "s", "is_active": "True"}
