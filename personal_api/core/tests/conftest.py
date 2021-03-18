# Here go your pytest fixtures, that can be used on your tests.
import logging

import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import CustomUser, Link
from core.tests.factories import UserModelFactory

logger = logging.getLogger(__name__)


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
def authenticated_api_client(
    real_user,
):  # pylint: disable=redefined-outer-name
    client = APIClient()
    refresh = RefreshToken.for_user(real_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture()
def anonymous_api_client():
    return APIClient()


@pytest.fixture()
def links_list():
    return [
        'https://www.redhat.com/sysadmin/getting-started-socat',
        'https://medium.com/aubergine-solutions/viewsets-in-django-rest-framework-25bb0110c210',
        'https://www.django-rest-framework.org/api-guide/viewsets/',
        'https://harrymoreno.com/2019/06/12/Overriding-Django-Rest-Framework-viewsets.html',
        'https://github.com/curl/curl',
        'https://dropbox.tech/infrastructure/atlas--our-journey-from-a-python-monolith-to-a-managed-platform',
    ]


@pytest.fixture
def setup_links_instances(links_list, setup_user_instances):
    User = get_user_model()
    assert User.objects.count() == 2

    for index, url in enumerate(links_list):
        is_even = index % 2 == 0
        user = User.objects.first() if is_even else User.objects.last()
        new_url = Link(original_link=url, user=user)
        new_url.save()

    return Link.objects.all()
