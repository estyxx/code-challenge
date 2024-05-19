import pytest

from challenge.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User) -> None:
    assert user.full_name == f"{user.first_name} {user.last_name}"
