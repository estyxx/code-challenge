import re

import pytest
from django.core.exceptions import ValidationError

from challenge.energy.models import MeterPoint

pytestmark = pytest.mark.django_db


class TestModelValidation:
    def test_meter_point_validation_status_invalid_raise_error(self):
        with pytest.raises(
            ValidationError,
            match=re.escape("Invalid ValidationStatus: W. (Allowed: F, U, V)"),
        ):
            MeterPoint.objects.create(mpan="1200023305967", validation_status="W")

    @pytest.mark.xfail()
    def test_meter_validation_invalid_reading_type_raise_error(self):
        pass
