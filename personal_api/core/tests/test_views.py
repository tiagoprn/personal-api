import factory
import pytest
from faker import Faker
from rest_framework.test import APIClient

from core.tests.factories import UrlModelFactory, UserModelFactory


@pytest.mark.django_db
class TestViewsSample:
    def setup(self):
        self.client = APIClient()

    def test_using_pytest_fixture_and_factory(self):
        urls = set()
        while len(urls) < 60:
            fake_url = Faker().uri()
            if len(fake_url) < 200:
                urls.add(fake_url)

        user = UserModelFactory()

        UrlModelFactory.create_batch(
            60,
            user=user,
            name=factory.Sequence(lambda n: n + 1),
            original_url=factory.Iterator(urls),
        )
        assert True


@pytest.mark.integration
class TestViewsIntegration:
    def test_integration(self):
        """
        This is an integration test that depends on external databases,
        slow services, etc. Use 'integration' marker to exclude them
        from normal tests
        """
        assert True


@pytest.mark.parametrize(
    "test_input,expected", [("3+5", 8), ("2+4", 6), ("3*3", 9)]
)
def test_with_parametrize_example(test_input, expected):
    assert eval(test_input) == expected  # pylint: disable=eval-used
