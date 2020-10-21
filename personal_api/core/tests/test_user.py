import pytest


@pytest.mark.django_db
def test_access_token_generation_must_pass_on_existing_user(
    real_user, anonymous_api_client
):
    credential_response = anonymous_api_client.post(
        '/api/token/', {'username': real_user.username, 'password': '12345678'}
    )
    assert credential_response.status_code == 200
    assert {'refresh', 'access'}.intersection(
        set(credential_response.json().keys())
    )


@pytest.mark.django_db
def test_access_to_authenticated_enpoint_must_pass_on_existing_user(
    real_user, authenticated_api_client
):
    response = authenticated_api_client.get('/core/greetings/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello there, hal_jordan!'}
