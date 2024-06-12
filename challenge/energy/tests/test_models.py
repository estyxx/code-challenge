from typing import TYPE_CHECKING

import pytest

from challenge.energy.models import EnergyConsumption

if TYPE_CHECKING:
    from challenge.energy.tests.factories import EnergyConsumptionFactory
    from challenge.users.models import User


pytestmark = pytest.mark.django_db


def test_energy_consumption_factory_works(
    energy_consumption_factory: "EnergyConsumptionFactory", user: "User"
) -> None:
    consumption = energy_consumption_factory(user=user)

    assert consumption
    assert EnergyConsumption.objects.filter(pk=consumption.pk).exists()
