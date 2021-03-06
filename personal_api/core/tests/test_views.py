import factory
import pytest
from rest_framework.test import APIClient

from .factories import SampleModelFactory


@pytest.mark.django_db
class TestViewsSample:
    def setup(self):
        self.client = APIClient()

    def test_using_pytest_fixture_and_factory(
        self, content_payload
    ):  # pylint: disable=unused-argument
        SampleModelFactory.create_batch(
            60, name=factory.Sequence(lambda n: n + 1)
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
