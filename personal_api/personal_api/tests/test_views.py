from unittest import mock

import pytest
from rest_framework.test import APIRequestFactory

from personal_api.views import (
    HealthcheckLiveness,
    HealthcheckReadiness,
)


class TestHealthCheckViews:
    @mock.patch('personal_api.views.get_app_version')
    @mock.patch('personal_api.views.get_last_migration')
    @pytest.mark.django_db
    def test_healthcheck_liveness(self, mocked_migration, mocked_version):
        mocked_version.return_value = '1.0'
        mocked_migration.return_value = 'testing'
        factory = APIRequestFactory()
        request = factory.get('/health-check/liveness', format='json')
        view = HealthcheckLiveness.as_view()

        response = view(request)
        response.render()

        assert 'live' in response.data.keys()
        assert 'version' in response.data.keys()
        assert response.data['version'] == '1.0'

    @mock.patch('personal_api.views.get_app_version')
    def test_healthcheck_readiness(self, mocked_version):
        mocked_version.return_value = '1.0'
        factory = APIRequestFactory()
        request = factory.get('/health-check/readiness', format='json')
        view = HealthcheckReadiness.as_view()

        response = view(request)
        response.render()

        assert 'ready' in response.data.keys()
        assert 'app_version' in response.data.keys()
        assert response.data['app_version'] == '1.0'
