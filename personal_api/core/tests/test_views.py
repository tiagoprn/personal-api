import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.mark.django_db
def test_access_to_greetings_endpoint_must_pass_on_existing_user(
    real_user, authenticated_api_client
):  # pylint: disable=unused-argument
    response = authenticated_api_client.get('/core/greetings/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello there, hal_jordan!'}


@pytest.mark.django_db
def test_access_to_greetings_endpoint_must_fail_on_anonymous_user(
    anonymous_api_client,
):
    response = anonymous_api_client.get('/core/greetings/')
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


@pytest.mark.django_db
class TestLinkViewSet:
    def authenticated_api_client(
        self, user
    ):  # pylint: disable=redefined-outer-name
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client

    def test_access_to_links_get_endpoint_must_fail_for_anonymous_user(
        self, anonymous_api_client
    ):
        response = anonymous_api_client.get('/core/api/links/')
        assert response.status_code == 401
        assert response.json() == {
            'detail': 'Authentication credentials were not provided.'
        }

    def test_links_get_endpoint_for_existing_users(
        self, setup_links_instances
    ):
        expected_users_links = {
            '1': [
                'https://www.redhat.com/sysadmin/getting-started-socat',
                'https://www.django-rest-framework.org/api-guide/viewsets/',
                'https://github.com/curl/curl',
            ],
            '2': [
                'https://medium.com/aubergine-solutions/viewsets-in-django-rest-framework-25bb0110c210',
                'https://harrymoreno.com/2019/06/12/Overriding-Django-Rest-Framework-viewsets.html',
                'https://dropbox.tech/infrastructure/atlas--our-journey-from-a-python-monolith-to-a-managed-platform',
            ],
        }
        assert setup_links_instances == expected_users_links

        for user in User.objects.all():
            client = self.authenticated_api_client(user=user)
            response = client.get('/core/api/links/')
            assert response.status_code == 200

            json_response = response.json()
            assert json_response['count'] == 3

            users = set(result['user'] for result in json_response['results'])
            assert users == {user.id}

            links = [
                result['original_link'] for result in json_response['results']
            ]
            assert set(links) == set(expected_users_links[str(user.id)])

    def test_links_post_endpoint_for_existing_users(
        self, setup_links_instances
    ):
        pass  # TODO
