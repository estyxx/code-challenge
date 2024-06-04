import pytest
from rest_framework.test import APIClient

from challenge.tasks.tests.factories import *  # noqa: F403
from challenge.users.tests.factories import *  # noqa: F403


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    """
    Fixture to provide an API client
    """
    return APIClient()
