# Here go your pytest fixtures, that can be used on your tests.
import pytest

from core.models import CustomUser
from core.tests.factories import UserModelFactory


@pytest.fixture
def content_payload():
    return {"name": "Hal Jordan", "complexity": "s", "is_active": "True"}


@pytest.fixture
def fake_user():
    return UserModelFactory(
        username='hal_jordan',
        email='haljordan@greenlanternscorp.com',
        password='12345678',
    )


@pytest.fixture
def real_user():
    user = CustomUser(
        username='hal_jordan', email='haljordan@greenlanternscorp.com'
    )
    user.set_password('12345678')
    user.save()
    return user
