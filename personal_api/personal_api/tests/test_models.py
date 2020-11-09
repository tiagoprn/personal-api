from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from freezegun import freeze_time

from core.models import Url


"""
IMPORTANT: use real model instances in these tests, not the model factory -
so to the ensure the models as working properly
"""


class TestModelManager:
    def setup_method(self):
        users, urls = self.get_test_data()
        User = get_user_model()

        new_users = []
        for user in users:
            new_user = User.objects.create_user(**user)
            new_user.save()
            new_users.append(new_user)

        for index, url in enumerate(urls, start=1):
            url_user = new_users[0] if index <= 4 else new_users[1]
            url['user'] = url_user
            new_url = Url.objects.create(**url)
            new_url.save()

    def teardown_method(self):
        # TODO: delete all test users and urls
        pass

    def get_test_data(self):
        users = [
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
        urls = [
            {
                'name': 'google',
                'original_url': 'https://www.google.com',
                'created_at': datetime(2020, 1, 1, 8, 0, 0),
                'updated_at': datetime(2020, 1, 1, 8, 0, 0),
            },
            {
                'name': 'bing',
                'original_url': 'https://www.bing.com',
                'created_at': datetime(2020, 1, 3, 8, 0, 0),
                'updated_at': datetime(2020, 1, 3, 8, 0, 0),
            },
            {
                'name': 'amazon',
                'original_url': 'https://www.amazon.com',
                'created_at': datetime(2020, 1, 8, 8, 0, 0),
                'updated_at': datetime(2020, 1, 8, 8, 0, 0),
            },
            {
                'name': 'somesite',
                'original_url': 'https://www.somesite.com',
                'created_at': datetime(2020, 1, 9, 8, 0, 0),
                'updated_at': datetime(2020, 1, 9, 8, 0, 0),
            },
            {
                'name': 'site1',
                'original_url': 'https://www.site1.com',
                'created_at': datetime(2020, 1, 12, 8, 0, 0),
                'updated_at': datetime(2020, 1, 12, 8, 0, 0),
            },
            {
                'name': 'site2',
                'original_url': 'https://www.site2.com',
                'created_at': datetime(2020, 1, 15, 8, 0, 0),
                'updated_at': datetime(2020, 1, 15, 8, 0, 0),
            },
            {
                'name': 'site3',
                'original_url': 'https://www.site3.com',
                'created_at': datetime(2020, 1, 18, 8, 0, 0),
                'updated_at': datetime(2020, 1, 18, 8, 0, 0),
            },
            {
                'name': 'site4',
                'original_url': 'https://www.site4.com',
                'created_at': datetime(2020, 1, 21, 8, 0, 0),
                'updated_at': datetime(2020, 1, 21, 8, 0, 0),
            },
            {
                'name': 'site5',
                'original_url': 'https://www.site5.com',
                'created_at': datetime(2020, 1, 24, 8, 0, 0),
                'updated_at': datetime(2020, 1, 24, 8, 0, 0),
            },
            {
                'name': 'site6',
                'original_url': 'https://www.site6.com',
                'created_at': datetime(2020, 1, 25, 8, 0, 0),
                'updated_at': datetime(2020, 1, 25, 8, 0, 0),
            },
        ]
        return users, urls

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'days,frozen_time,url_names',
        [(5, '2020/01/05 08:00:00', ['bing', 'google'])],
    )
    # TODO: add more records do parametrize above, and fix this failing test
    def test_most_recent_filter(self, days, frozen_time, url_names):
        User = get_user_model()
        assert User.objects.count() == 2
        assert Url.objects.count() == 10

        with freeze_time(frozen_time):
            most_recent_urls_names = Url.objects.most_recent(
                days=days
            ).values_list('name', flat=True)
            assert most_recent_urls_names == url_names

    def test_from_user_filter(self):
        # TODO
        # user_urls = Url.objects.from_user(user=user)
        pass

    def test_most_recent_and_from_user_filters_together(self):
        # TODO
        # user_most_recent_urls = Url.objects.from_user(
        #     user=user).most_recent(days=1)
        pass
