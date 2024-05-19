import factory
from factory import Faker
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from challenge.users.models import User


@register
class UserFactory(DjangoModelFactory):
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "test")

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None) -> None:  # type: ignore
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()

    class Meta:
        model = User
        django_get_or_create = ["email"]
