import pytest
from django.contrib.auth import get_user_model
from freezegun import freeze_time

from core.models import Url


@pytest.mark.django_db
@pytest.mark.parametrize(
    'days,frozen_time,url_names',
    [
        (5, '2020/01/05 08:00:00', ['bing', 'google']),
        (10, '2020/01/10 08:00:00', ['bing', 'google', 'amazon', 'somesite']),
        (2, '2020/01/25 08:00:00', ['site5', 'site6']),
        (
            25,
            '2020/01/25 08:00:00',
            [
                'bing',
                'google',
                'amazon',
                'somesite',
                'site1',
                'site2',
                'site3',
                'site4',
                'site5',
                'site6',
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
        'atrocitus': ['google', 'bing', 'amazon', 'somesite'],
        'haljordan': ['site1', 'site2', 'site3', 'site4', 'site5', 'site6'],
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
        'atrocitus': ['amazon', 'somesite'],
        'haljordan': ['site4', 'site5', 'site6'],
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
