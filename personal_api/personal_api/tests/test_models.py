from django.contrib.auth import get_user_model

import pytest
from freezegun import freeze_time

from core.models import Link


@pytest.mark.django_db
class TestFilter:
    @pytest.mark.parametrize(
        'days,frozen_time,url_names',
        [
            (5, '2020/01/05 08:00:00', ['bing', 'ubuntu']),
            (
                10,
                '2020/01/10 08:00:00',
                ['bing', 'ubuntu', 'destinationlinux', 'jupiterbroadcasting'],
            ),
            (2, '2020/01/25 08:00:00', ['trello']),
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
                ],
            ),
        ],
    )  # pylint: disable=too-many-arguments
    def test_recently_updated_filter(
        self, setup_model_instances, days, frozen_time, url_names
    ):  # pylint: disable=unused-argument
        User = get_user_model()
        assert User.objects.count() == 2
        assert Link.objects.count() == 9

        with freeze_time(frozen_time):
            recently_updated_urls_names = Link.objects.recently_updated(
                days=days
            ).values_list('name', flat=True)
            assert set(recently_updated_urls_names) == set(url_names)

    def test_from_user_filter(
        self, setup_model_instances
    ):  # pylint: disable=unused-argument
        User = get_user_model()
        assert User.objects.count() == 2
        assert Link.objects.count() == 9

        usernames = ['atrocitus', 'haljordan']
        expected_user_urls = {
            'atrocitus': [
                'ubuntu',
                'bing',
                'destinationlinux',
                'jupiterbroadcasting',
            ],
            'haljordan': ['github', 'gitlab', 'jira', 'atlassian', 'trello'],
        }
        for username in usernames:
            user = User.objects.filter(username=username).first()
            urls = Link.objects.from_user(user=user).values_list(
                'name', flat=True
            )
            assert set(urls) == set(expected_user_urls[username])

    def test_most_recent_and_from_user_filters_together(
        self, setup_model_instances
    ):  # pylint: disable=unused-argument
        User = get_user_model()
        assert User.objects.count() == 2
        assert Link.objects.count() == 9

        usernames = ['atrocitus', 'haljordan']
        most_recent_filters = {
            'atrocitus': {'frozen_time': '2020/01/09 08:00:00', 'days': 5},
            'haljordan': {'frozen_time': '2020/01/25 08:00:00', 'days': 5},
        }
        expected_user_urls = {
            'atrocitus': ['destinationlinux', 'jupiterbroadcasting'],
            'haljordan': ['atlassian', 'trello'],
        }
        for username in usernames:
            user = User.objects.filter(username=username).first()
            frozen_time = most_recent_filters[username]['frozen_time']
            days = most_recent_filters[username]['days']
            with freeze_time(frozen_time):
                urls = Link.objects.recently_updated(
                    days=days, user=user
                ).values_list('name', flat=True)
                assert set(urls) == set(expected_user_urls[username])


@pytest.mark.django_db
def test_search_by_partial_shortened_hash(
    setup_model_instances
):  # pylint: disable=unused-argument
    User = get_user_model()
    assert User.objects.count() == 2
    assert Link.objects.count() == 9

    all_hashes = []
    for url in Link.objects.all():
        assert url.id
        short_hash = url.shortened_hash
        assert short_hash
        all_hashes.append({short_hash: url.slug})

    for hash_dict in all_hashes:
        key = list(hash_dict.keys())[0]

        start_key = key[:11]
        middle_key = key[7:17]
        end_key = key[11:]

        url_instance_with_start_key = Link.objects.filter(
            shortened_hash__contains=start_key
        ).first()

        url_instance_with_middle_key = Link.objects.filter(
            shortened_hash__contains=middle_key
        ).first()

        url_instance_with_end_key = Link.objects.filter(
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
def test_get_domain_property_value(
    setup_model_instances
):  # pylint: disable=unused-argument
    User = get_user_model()
    assert User.objects.count() == 2
    assert Link.objects.count() == 9

    domains = {}
    for url in Link.objects.all():
        domains[url.sanitized_link] = url.domain

    expected_domains = {
        'https://ubuntu.com': 'ubuntu.com',
        'https://www.bing.com': 'www.bing.com',
        'https://destinationlinux.org': 'destinationlinux.org',
        'https://www.jupiterbroadcasting.com': 'www.jupiterbroadcasting.com',
        'https://github.com': 'github.com',
        'https://about.gitlab.com': 'about.gitlab.com',
        'https://www.atlassian.com/software/jira': 'www.atlassian.com',
        'https://www.atlassian.com': 'www.atlassian.com',
        'https://trello.com': 'trello.com',
    }

    assert domains == expected_domains


@pytest.mark.django_db
def test_set_name_from_url_when_name_empty(
    setup_user_instances
):  # pylint: disable=unused-argument
    User = get_user_model()
    assert User.objects.count() == 2

    urls = (
        'https://johnlekberg.com/blog/2020-11-27-cli-pandoc.html',
        'https://github.com/andy-landy/traceback_with_variables#colors',
        'https://jon.bo/posts/digital-tools/',
        'https://danishpraka.sh/2020/02/23/journaling-in-vim.html',
        'https://danishpraka.sh/',
        'https://github.com/danishprakash/vimport',
    )

    for url in urls:
        new_url = Link(original_link=url, user=User.objects.first())
        new_url.save()

    names = [link.name for link in Link.objects.all()]

    expected_names = [
        'johnlekberg.com 2020-11-27-cli-pandoc.html',
        'github.com traceback_with_variables#colors',
        'jon.bo digital-tools',
        'danishpraka.sh journaling-in-vim.html',
        'danishpraka.sh',
        'github.com vimport',
    ]

    assert set(names) == set(expected_names)

    Link.objects.all().delete()
