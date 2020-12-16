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
def test_access_token_generation_must_fail_on_non_existing_user(
    anonymous_api_client,
):
    credential_response = anonymous_api_client.post(
        '/api/token/', {'username': 'john_doe', 'password': '12345678'}
    )
    assert credential_response.status_code == 401
    assert credential_response.json() == {
        'detail': 'No active account found with the given credentials'
    }
