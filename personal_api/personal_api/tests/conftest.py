# Here go your pytest fixtures, that can be used on your tests.
import logging
from datetime import datetime

from django.contrib.auth import get_user_model

import pytest
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


# pylint: disable=line-too-long
@pytest.fixture()
def real_urls():
    return [
        {
            'original': 'https://programmingdigest.net/?utm_source=techleaddigest&utm_medium=email&utm_campaign=footer',
            'sanitized': 'https://programmingdigest.net',
        },
        {
            'original': 'https://techleaddigest.net/links/9298/redirect?subscriber_id=deac88e2-c797-4ba8-bae1-87423cd78d80&utm_medium=email',
            'sanitized': 'https://productcoalition.com/product-thinking-vs-project-thinking-380692a2d4e',
        },
        {
            'original': 'https://login.folha.com.br/assinatura/400508?utm_source=roi360&utm_medium=EDFSP&utm_campaign=Fornecedor_ROI_EDFSP',
            'sanitized': 'https://login.folha.com.br/assinatura/400508',
        },
        {
            'original': 'https://click.mlsend.com/link/c/YT0xNTUzNDg0MTMzNTkyNzI4NzQyJmM9bDBjNCZlPTUxOTUwNzQ5JmI9NDUzMzU5OTcyJmQ9ZTFvNGUxaA==.ZGx3fsABcnMregPCd51Z0jxi0O6KVn4fdz6KPifYCI0',
            'sanitized': 'https://itsfoss.com/mudita-os',
        },
        {
            'original': 'https://click.mlsend.com/link/c/YT0xNTUzNDg0MTMzNTkyNzI4NzQyJmM9bDBjNCZlPTUxOTUwNzQ5JmI9NDUzMzU5OTc4JmQ9eTh1M3M1dQ==.MMQ2OkLlwVDNtTd51thXUWXt0DLzBABdvbu391cmD6Q',
            'sanitized': 'https://itsfoss.com/linux-release-roundup',
        },
    ]


@pytest.fixture
def urls_data():
    return [
        {
            'name': 'ubuntu',
            'original_url': 'https://www.ubuntu.com',
            'frozen_timestamp': datetime(2020, 1, 1, 8, 0, 0),
        },
        {
            'name': 'bing',
            'original_url': 'https://www.bing.com',
            'frozen_timestamp': datetime(2020, 1, 3, 8, 0, 0),
        },
        {
            'name': 'destinationlinux',
            'original_url': 'https://destinationlinux.org',
            'frozen_timestamp': datetime(2020, 1, 8, 8, 0, 0),
        },
        {
            'name': 'jupiterbroadcasting',
            'original_url': 'https://www.jupiterbroadcasting.com',
            'frozen_timestamp': datetime(2020, 1, 9, 8, 0, 0),
        },
        {
            'name': 'github',
            'original_url': 'https://www.github.com',
            'frozen_timestamp': datetime(2020, 1, 12, 8, 0, 0),
        },
        {
            'name': 'gitlab',
            'original_url': 'https://www.gitlab.com',
            'frozen_timestamp': datetime(2020, 1, 15, 8, 0, 0),
        },
        {
            'name': 'jira',
            'original_url': 'https://www.jira.com',
            'frozen_timestamp': datetime(2020, 1, 18, 8, 0, 0),
        },
        {
            'name': 'atlassian',
            'original_url': 'https://www.atlassian.com',
            'frozen_timestamp': datetime(2020, 1, 21, 8, 0, 0),
        },
        {
            'name': 'trello',
            'original_url': 'https://trello.com',
            'frozen_timestamp': datetime(2020, 1, 24, 8, 0, 0),
        },
        {
            'name': 'archlinux',
            'original_url': 'https://www.archlinux.org',
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
