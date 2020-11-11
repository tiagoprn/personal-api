# Here go your pytest fixtures, that can be used on your tests.
import logging
from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from freezegun import freeze_time

from core.models import Url

logger = logging.getLogger(__name__)


@pytest.fixture
def users_data():
    return [
        {
            'username': 'atrocitus',
            'email': 'atrocitus@atrocitus.com',
            'password': 'whatever+1',
        },
        {
            'username': 'haljordan',
            'email': 'haljordan@greenlanterns.com',
            'password': 'whatever+2',
        },
    ]


@pytest.fixture
def urls_data():
    return [
        {
            'name': 'google',
            'original_url': 'https://www.google.com',
            'frozen_timestamp': datetime(2020, 1, 1, 8, 0, 0),
        },
        {
            'name': 'bing',
            'original_url': 'https://www.bing.com',
            'frozen_timestamp': datetime(2020, 1, 3, 8, 0, 0),
        },
        {
            'name': 'amazon',
            'original_url': 'https://www.amazon.com',
            'frozen_timestamp': datetime(2020, 1, 8, 8, 0, 0),
        },
        {
            'name': 'somesite',
            'original_url': 'https://www.somesite.com',
            'frozen_timestamp': datetime(2020, 1, 9, 8, 0, 0),
        },
        {
            'name': 'site1',
            'original_url': 'https://www.site1.com',
            'frozen_timestamp': datetime(2020, 1, 12, 8, 0, 0),
        },
        {
            'name': 'site2',
            'original_url': 'https://www.site2.com',
            'frozen_timestamp': datetime(2020, 1, 15, 8, 0, 0),
        },
        {
            'name': 'site3',
            'original_url': 'https://www.site3.com',
            'frozen_timestamp': datetime(2020, 1, 18, 8, 0, 0),
        },
        {
            'name': 'site4',
            'original_url': 'https://www.site4.com',
            'frozen_timestamp': datetime(2020, 1, 21, 8, 0, 0),
        },
        {
            'name': 'site5',
            'original_url': 'https://www.site5.com',
            'frozen_timestamp': datetime(2020, 1, 24, 8, 0, 0),
        },
        {
            'name': 'site6',
            'original_url': 'https://www.site6.com',
            'frozen_timestamp': datetime(2020, 1, 25, 8, 0, 0),
        },
    ]


@pytest.fixture()
@pytest.mark.django_db
def setup_model_instances(urls_data, users_data):
    logger.info('setup')

    User = get_user_model()

    new_users = []
    for user in users_data:
        new_user = User.objects.create_user(**user)
        new_user.save()
        new_users.append(new_user)

    for index, url in enumerate(urls_data, start=1):
        url_user = new_users[0] if index <= 4 else new_users[1]
        url['user'] = url_user
        frozen_timestamp = url.pop('frozen_timestamp').strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        with freeze_time(frozen_timestamp):
            new_url = Url.objects.create(**url)
            new_url.save()

    yield

    logger.info('teardown')

    Url.objects.all().delete()
    User.objects.all().delete()
