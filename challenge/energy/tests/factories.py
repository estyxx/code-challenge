import factory
from factory import Faker
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from pytest_factoryboy import register

from challenge.energy.models import EnergyConsumption


@register
class EnergyConsumptionFactory(DjangoModelFactory):
    timestamp = Faker("date_time_between", start_date="-1y", end_date="now")
    consumption = Faker("pyfloat", positive=True, max_value=99999)
    source = FuzzyChoice(choices=EnergyConsumption.Source.choices)
    uploaded_by = factory.SubFactory("challenge.users.tests.factories.UserFactory")

    class Meta:
        model = EnergyConsumption
