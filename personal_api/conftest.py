import json
import logging
import uuid
from datetime import datetime, timedelta
from unittest import mock

from django.contrib.auth import get_user_model

import pytest
from freezegun import freeze_time
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import CustomUser, Link
from core.serializers import LinkSerializer
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
def uuids():
    fixed_uuids = [
        '7b5bd93b-0aa2-4879-8aa4-262318d503a0',
        '69c082fe-fa66-4f5e-b784-84be5d5a1817',
        'd85eace6-6443-4b0d-9a01-7ec7f7c6c9c8',
        '9304e4a9-93fc-4e97-9177-32e8518782e8',
        '239812fe-0b6d-4d33-b21e-e5c5cbd67656',
        '4cde0dba-67b3-43fb-b402-c966611cbf6d',
        '1353ff2c-e86e-41f3-8b09-84031f8405d1',
        'ce4171f7-1792-402a-8204-cfa9419147fe',
        '4cb89ff1-2ad3-49ff-909d-f2b23cf2817e',
        '44519977-a701-4c3b-8ed6-53d4dce9a05c',
    ]

    return [uuid.UUID(value) for value in fixed_uuids]


@pytest.fixture
@mock.patch('core.services.links.resolve_url', return_value='')
def setup_links_instances(
    mocked_resolve_url, links_list, setup_user_instances, uuids
):
    User = get_user_model()
    assert User.objects.count() == 2

    users_links = {}

    with open('/tmp/temptestfile.txt', 'w+') as temp_test_file:
        reference_date = datetime.strptime(
            '2021-01-01 08:00:00', '%Y-%m-%d %H:%M:%S'
        )
        for index, url in enumerate(links_list):
            is_even = index % 2 == 0
            user = User.objects.first() if is_even else User.objects.last()

            reference_date = reference_date + timedelta(days=3)
            frozen_timestamp = reference_date.strftime('%Y-%m-%d %H:%M:%S')
            with freeze_time(frozen_timestamp):
                new_url = Link(original_link=url, user=user)
                new_url.id = uuids[index]
                new_url.save()

            if str(user.id) not in users_links.keys():
                users_links[str(user.id)] = []

            serialized_url_dict = LinkSerializer(new_url).data

            temp_test_file.write(
                f'Adding link for username={user.username}: '
                f'{json.dumps(serialized_url_dict)}\n'
            )

            users_links[str(user.id)].append(serialized_url_dict)

    return users_links


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
            'original_link': 'https://www.ubuntu.com',
            'frozen_timestamp': datetime(2020, 1, 1, 8, 0, 0),
        },
        {
            'name': 'bing',
            'original_link': 'https://www.bing.com',
            'frozen_timestamp': datetime(2020, 1, 3, 8, 0, 0),
        },
        {
            'name': 'destinationlinux',
            'original_link': 'https://destinationlinux.org',
            'frozen_timestamp': datetime(2020, 1, 8, 8, 0, 0),
        },
        {
            'name': 'jupiterbroadcasting',
            'original_link': 'https://www.jupiterbroadcasting.com',
            'frozen_timestamp': datetime(2020, 1, 9, 8, 0, 0),
        },
        {
            'name': 'github',
            'original_link': 'https://www.github.com',
            'frozen_timestamp': datetime(2020, 1, 12, 8, 0, 0),
        },
        {
            'name': 'gitlab',
            'original_link': 'https://www.gitlab.com',
            'frozen_timestamp': datetime(2020, 1, 15, 8, 0, 0),
        },
        {
            'name': 'jira',
            'original_link': 'https://www.jira.com',
            'frozen_timestamp': datetime(2020, 1, 18, 8, 0, 0),
        },
        {
            'name': 'atlassian',
            'original_link': 'https://www.atlassian.com',
            'frozen_timestamp': datetime(2020, 1, 21, 8, 0, 0),
        },
        {
            'name': 'trello',
            'original_link': 'https://trello.com',
            'frozen_timestamp': datetime(2020, 1, 24, 8, 0, 0),
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
            new_url = Link.objects.create(**url)
            new_url.save()

    yield

    logger.info('teardown')

    Link.objects.all().delete()
    User.objects.all().delete()


@pytest.fixture()
@pytest.mark.django_db
def setup_user_instances(users_data):
    logger.info('setup')

    User = get_user_model()

    for user in users_data:
        new_user = User.objects.create_user(**user)
        new_user.save()

    yield

    logger.info('teardown')

    User.objects.all().delete()
