import pytest


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
def test_access_to_links_get_endpoint_must_fail_on_anonymous_user(
    anonymous_api_client,
):
    response = anonymous_api_client.get('/core/api/links/')
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }
