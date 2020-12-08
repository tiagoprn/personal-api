from django.contrib.auth import get_user_model

import pytest
from freezegun import freeze_time

from core.models import Url


@pytest.mark.django_db
@pytest.mark.parametrize(
    'days,frozen_time,url_names',
    [
        (5, '2020/01/05 08:00:00', ['bing', 'google']),
        (
            10,
            '2020/01/10 08:00:00',
            ['bing', 'google', 'destinationlinux', 'jupiterbroadcasting'],
        ),
        (2, '2020/01/25 08:00:00', ['trello', 'archlinux']),
        (
            25,
            '2020/01/25 08:00:00',
            [
                'bing',
                'google',
                'destinationlinux',
                'jupiterbroadcasting',
                'github',
                'gitlab',
                'jira',
                'atlassian',
                'trello',
                'archlinux',
            ],
        ),
    ],
)  # pylint: disable=too-many-arguments
def test_recently_updated_filter(
    setup_model_instances, days, frozen_time, url_names
):  # pylint: disable=unused-argument
    User = get_user_model()
    assert User.objects.count() == 2
    assert Url.objects.count() == 10

    with freeze_time(frozen_time):
        recently_updated_urls_names = Url.objects.recently_updated(
            days=days
        ).values_list('name', flat=True)
        assert set(recently_updated_urls_names) == set(url_names)


@pytest.mark.django_db
def test_from_user_filter(
    setup_model_instances
):  # pylint: disable=unused-argument
    User = get_user_model()
    assert User.objects.count() == 2
    assert Url.objects.count() == 10

    usernames = ['atrocitus', 'haljordan']
    expected_user_urls = {
        'atrocitus': [
            'google',
            'bing',
            'destinationlinux',
            'jupiterbroadcasting',
        ],
        'haljordan': [
            'github',
            'gitlab',
            'jira',
            'atlassian',
            'trello',
            'archlinux',
        ],
    }
    for username in usernames:
        user = User.objects.filter(username=username).first()
        urls = Url.objects.from_user(user=user).values_list('name', flat=True)
        assert set(urls) == set(expected_user_urls[username])


@pytest.mark.django_db
def test_most_recent_and_from_user_filters_together(
    setup_model_instances
):  # pylint: disable=unused-argument
    User = get_user_model()
    assert User.objects.count() == 2
    assert Url.objects.count() == 10

    usernames = ['atrocitus', 'haljordan']
    most_recent_filters = {
        'atrocitus': {'frozen_time': '2020/01/09 08:00:00', 'days': 5},
        'haljordan': {'frozen_time': '2020/01/25 08:00:00', 'days': 5},
    }
    expected_user_urls = {
        'atrocitus': ['destinationlinux', 'jupiterbroadcasting'],
        'haljordan': ['atlassian', 'trello', 'archlinux'],
    }
    for username in usernames:
        user = User.objects.filter(username=username).first()
        frozen_time = most_recent_filters[username]['frozen_time']
        days = most_recent_filters[username]['days']
        with freeze_time(frozen_time):
            urls = Url.objects.recently_updated(
                days=days, user=user
            ).values_list('name', flat=True)
            assert set(urls) == set(expected_user_urls[username])


@pytest.mark.django_db
def test_search_by_shortened_hash(
    setup_model_instances
):  # pylint: disable=unused-argument
    User = get_user_model()
    assert User.objects.count() == 2
    assert Url.objects.count() == 10

    all_hashes = {}
    for url in Url.objects.all():
        assert url.id
        short_hash = url.shortened_hash
        assert short_hash
        all_hashes.append({short_hash: url.slug})

    __import__('ipdb').set_trace()

    # TODO: scenarios: exact string and partial string, with "ilike", etc...
    # - so that we can be able to search for the smallest hash possible


@pytest.mark.django_db
def test_get_domain_property_value(
    setup_model_instances
):  # pylint: disable=unused-argument
    assert False  # TODO
