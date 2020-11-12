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
    # TODO
    # user_urls = Url.objects.from_user(user=user)
    pass


@pytest.mark.django_db
def test_most_recent_and_from_user_filters_together(
    setup_model_instances
):  # pylint: disable=unused-argument
    # TODO
    # user_most_recent_urls = Url.objects.from_user(
    #     user=user).most_recent(days=1)
    pass
