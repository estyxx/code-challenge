import datetime
from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone

from challenge.energy.models import Meter, MeterPoint, Reading

pytestmark = pytest.mark.django_db


class TestCommandImportFlow:
    def test_happy_path(self, valid_uff_file):
        out = StringIO()

        call_command("import_flow", valid_uff_file, stdout=out)

        assert "Successfully imported" in out.getvalue()
        assert (meter_point_1 := MeterPoint.objects.get(mpan="1200023305967"))
        assert meter_point_1.validation_status == MeterPoint.ValidationStatus.VALIDATED

        assert (meter_1 := Meter.objects.get(meter_id="F75A 00802"))
        assert meter_1.meter_point == meter_point_1
        assert meter_1.reading_type == Meter.ReadingType.D

        assert (
            reading_1 := Reading.objects.get(
                meter_register_id="S", register_reading=56311.0
            )
        )
        assert reading_1.meter_point == meter_point_1
        assert reading_1.meter == meter_1
        assert reading_1.reading_at == timezone.make_aware(
            datetime.datetime.strptime("20160222000000", "%Y%m%d%H%M%S"),
        )
        assert reading_1.md_reset_at is None
        assert reading_1.md_resets_number == 0
        assert reading_1.meter_reading_flag == Reading.Flag.VALID
        assert reading_1.reading_method == Reading.Method.N

    def test_execute_two_times_did_not_create_multiple_entries(self, valid_uff_file):
        out1 = StringIO()
        out2 = StringIO()
        file_name = valid_uff_file.split("/")[-1]
        call_command("import_flow", valid_uff_file, stdout=out1)

        with pytest.raises(
            CommandError,
            match=f"The flow file '{file_name}' has already been imported. Aborting.",
        ):
            call_command("import_flow", valid_uff_file, stdout=out2)


class TestFileValidation:
    def test_call_without_file_fails(
        self,
    ):
        out = StringIO()

        with pytest.raises(
            CommandError, match="the following arguments are required: file"
        ):
            call_command("import_flow", stdout=out)

    def test_file_not_found_raises_error(self):
        out = StringIO()

        with pytest.raises(CommandError, match='File "/file/path" not found'):
            call_command("import_flow", "/file/path", stdout=out)

    @pytest.mark.xfail()
    def test_invalid_header_raises_error(self, invalid_format_file):
        assert False

    def test_empty_file_raises_error(self, empty_file):
        out = StringIO()

        with pytest.raises(CommandError, match="File is empty"):
            call_command("import_flow", empty_file, stdout=out)
