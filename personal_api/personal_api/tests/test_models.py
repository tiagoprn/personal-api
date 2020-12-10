from django.contrib.auth import get_user_model

import pytest
from freezegun import freeze_time

from core.models import Url


# @pytest.mark.vcr
@pytest.mark.django_db
@pytest.mark.parametrize(
    'days,frozen_time,url_names',
    [
        (5, '2020/01/05 08:00:00', ['bing', 'ubuntu']),
        (
            10,
            '2020/01/10 08:00:00',
            ['bing', 'ubuntu', 'destinationlinux', 'jupiterbroadcasting'],
        ),
        (2, '2020/01/25 08:00:00', ['trello', 'archlinux']),
        (
            25,
            '2020/01/25 08:00:00',
            [
                'bing',
                'ubuntu',
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
# @pytest.mark.vcr
def test_from_user_filter(
    setup_model_instances
):  # pylint: disable=unused-argument
    User = get_user_model()
    assert User.objects.count() == 2
    assert Url.objects.count() == 10

    usernames = ['atrocitus', 'haljordan']
    expected_user_urls = {
        'atrocitus': [
            'ubuntu',
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
# @pytest.mark.vcr
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
# @pytest.mark.vcr
def test_search_by_partial_shortened_hash(
    setup_model_instances
):  # pylint: disable=unused-argument
    User = get_user_model()
    assert User.objects.count() == 2
    assert Url.objects.count() == 10

    all_hashes = []
    for url in Url.objects.all():
        assert url.id
        short_hash = url.shortened_hash
        assert short_hash
        all_hashes.append({short_hash: url.slug})

    for hash_dict in all_hashes:
        key = list(hash_dict.keys())[0]

        start_key = key[:11]
        middle_key = key[7:17]
        end_key = key[11:]

        url_instance_with_start_key = Url.objects.filter(
            shortened_hash__contains=start_key
        ).first()

        url_instance_with_middle_key = Url.objects.filter(
            shortened_hash__contains=middle_key
        ).first()

        url_instance_with_end_key = Url.objects.filter(
            shortened_hash__contains=end_key
        ).first()

        url_instances = [
            url_instance_with_start_key,
            url_instance_with_middle_key,
            url_instance_with_end_key,
        ]
        for instance in url_instances:
            assert instance.shortened_hash == key


@pytest.mark.django_db
# @pytest.mark.vcr
def test_get_domain_property_value(
    setup_model_instances
):  # pylint: disable=unused-argument
    assert False  # TODO
