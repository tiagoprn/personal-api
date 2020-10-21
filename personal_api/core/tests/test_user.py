import pytest
from django.test import Client
from rest_framework.test import APIClient

client = Client()


@pytest.mark.django_db
def test_access_token_on_greetings_authenticated_endpoint(real_user):
    # token generation
    credential_response = client.post(
        '/api/token/', {'username': real_user.username, 'password': '12345678'}
    )
    assert credential_response.status_code == 200

    credential_response_as_json = credential_response.json()
    assert {'refresh', 'access'}.intersection(
        set(credential_response_as_json.keys())
    )

    # use token at authenticated greetings endpoint
    # curl http://localhost:8000/core/greetings/ -H "Authorization: Bearer $(token)"
    token = credential_response_as_json['access']
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    greetings_authenticated_response = api_client.get('/core/greetings/')
    assert greetings_authenticated_response.status_code == 200
