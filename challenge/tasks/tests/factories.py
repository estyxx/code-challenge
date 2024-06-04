from factory import Faker, fuzzy
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from challenge.tasks.models import Task


@register
class TaskFactory(DjangoModelFactory):
    title = Faker("sentence")
    description = Faker("paragraph")
    status = fuzzy.FuzzyChoice(Task.Status)
    priority = fuzzy.FuzzyChoice(Task.Priority)
    due_date = Faker("future_date")

    class Meta:
        model = Task
        django_get_or_create = ["title"]
