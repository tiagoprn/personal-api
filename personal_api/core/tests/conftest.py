# Here go your pytest fixtures, that can be used on your tests.
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import CustomUser
from core.tests.factories import UserModelFactory


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


@pytest.fixture()
def authenticated_api_client(real_user):
    client = APIClient()
    refresh = RefreshToken.for_user(real_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture()
def anonymous_api_client():
    return APIClient()
