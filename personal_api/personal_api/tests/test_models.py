import pytest
from django.contrib.auth import get_user_model

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
            {'name': 'google', 'original_url': 'https://www.google.com'},
            {'name': 'bing', 'original_url': 'https://www.bing.com'},
            {'name': 'amazon', 'original_url': 'https://www.amazon.com'},
            {'name': 'somesite', 'original_url': 'https://www.somesite.com'},
            {'name': 'site1', 'original_url': 'https://www.site1.com'},
            {'name': 'site2', 'original_url': 'https://www.site2.com'},
            {'name': 'site3', 'original_url': 'https://www.site3.com'},
            {'name': 'site4', 'original_url': 'https://www.site4.com'},
            {'name': 'site5', 'original_url': 'https://www.site5.com'},
            {'name': 'site6', 'original_url': 'https://www.site6.com'},
        ]
        return users, urls

    @pytest.mark.django_db
    def test_most_recent_filter(self):
        User = get_user_model()
        assert User.objects.count() == 2
        assert Url.objects.count() == 10

        # TODO
        # most_recent_urls = Url.objects.most_recent(days=1)

    def test_from_user_filter(self):
        # TODO
        # user_urls = Url.objects.from_user(user=user)
        pass

    def test_most_recent_and_from_user_filters_together(self):
        # TODO
        # user_most_recent_urls = Url.objects.from_user(
        #     user=user).most_recent(days=1)
        pass
