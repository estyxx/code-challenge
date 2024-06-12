import factory
from django.conf import settings
from factory import Faker
from factory.django import DjangoModelFactory
from pytest_factoryboy import register


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
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ["email"]
