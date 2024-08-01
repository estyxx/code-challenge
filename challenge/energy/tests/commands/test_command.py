import re
from io import StringIO

import pytest
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError

pytestmark = pytest.mark.django_db


class TestCommandImportEnergyConsumption:
    def test_happy_path(self, valid_csv_file):
        out = StringIO()

        call_command("import_flow", valid_csv_file, stdout=out)

        assert "Successfully imported" in out.getvalue()
        # assert (business_a := Business.objects.get(name="Business A"))
        # assert business_a.name == "Business A"
        # assert business_a.address == "123 Business St"
        # assert business_a.contact_email == "businessa@example.com"

        # assert (business_b := Business.objects.get(name="Business B"))
        # assert business_b.name == "Business B"
        # assert business_b.address == "456 Enterprise Rd"
        # assert business_b.contact_email == "businessb@example.com"

        # assert (
        #     consumption_1 := EnergyConsumption.objects.get(
        #         date="2023-07-15",
        #         consumption_kwh=150.5,
        #         source=EnergyConsumption.Source.SOLAR,
        #     )
        # )
        # assert consumption_1.business == business_a

        # assert (
        #     consumption_2 := EnergyConsumption.objects.get(
        #         date="2023-07-15",
        #         consumption_kwh=200.75,
        #         source=EnergyConsumption.Source.WIND,
        #     )
        # )
        # assert consumption_2.business == business_b

        # assert (
        #     consumption_3 := EnergyConsumption.objects.get(
        #         date="2023-07-16",
        #         consumption_kwh=160.3,
        #         source=EnergyConsumption.Source.GRID,
        #     )
        # )
        # assert consumption_3.business == business_a

    def test_execute_two_times(self, valid_csv_file):
        out1 = StringIO()
        out2 = StringIO()

        call_command("import_flow", valid_csv_file, stdout=out1)
        call_command("import_flow", valid_csv_file, stdout=out2)

        assert 'Successfully imported "3" energy consumptions' in out1.getvalue()
        assert 'Successfully imported "0" energy consumptions' in out2.getvalue()


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

    def test_invalid_columns_raises_error(self, invalid_format_file):
        out = StringIO()

        with pytest.raises(
            CommandError,
            match=re.escape(
                "The file does not have the correct columns or the correct order.\n"
                "Expected: ['business_name', 'address', 'contact_email', 'date', 'consumption_kwh', 'source']\n"
                "Actual: ['name', 'location', 'email', 'timestamp', 'usage', 'origin']\n"
            ),
        ):
            call_command("import_flow", invalid_format_file, stdout=out)

    def test_empty_file_raises_error(self, empty_file):
        out = StringIO()

        with pytest.raises(CommandError, match=f'File "{empty_file}" is empty'):
            call_command("import_flow", empty_file, stdout=out)

    def test_csv_with_invalid_dates_raises_error_and_rollback(
        self, invalid_dates_csv_file
    ):
        out = StringIO()

        with pytest.raises(
            ValidationError,
            match="“15-07-2023” value has an invalid date format. It must be in YYYY-MM-DD format.",
        ):
            call_command("import_flow", invalid_dates_csv_file, stdout=out)

        # assert not Business.objects.filter(name="Business A").exists()
        # assert not Business.objects.filter(name="Business B").exists()
        # assert not EnergyConsumption.objects.filter(
        #     date="2023-07-15",
        #     consumption_kwh=150.5,
        #     source=EnergyConsumption.Source.SOLAR,
        # ).exists()
        # assert not EnergyConsumption.objects.filter(
        #     date="2023-07-15",
        #     consumption_kwh=200.75,
        #     source=EnergyConsumption.Source.WIND,
        # ).exists()
        # assert not EnergyConsumption.objects.filter(
        #     date="2023-07-16",
        #     consumption_kwh=160.3,
        #     source=EnergyConsumption.Source.GRID,
        # ).exists()

    def test_csv_invalid_source_raise_error_and_rollback(self, invalid_source_csv_file):
        out = StringIO()

        with pytest.raises(
            ValidationError,
            match="Invalid source: fire",
        ):
            call_command("import_flow", invalid_source_csv_file, stdout=out)

        # assert not Business.objects.filter(name="Business A").exists()
        # assert not Business.objects.filter(name="Business B").exists()
        # assert not EnergyConsumption.objects.filter(
        #     date="2023-07-15",
        #     consumption_kwh=150.5,
        #     source=EnergyConsumption.Source.SOLAR,
        # ).exists()
        # assert not EnergyConsumption.objects.filter(
        #     date="2023-07-15",
        #     consumption_kwh=200.75,
        #     source="fire",
        # ).exists()
        # assert not EnergyConsumption.objects.filter(
        #     date="2023-07-16",
        #     consumption_kwh=160.3,
        #     source=EnergyConsumption.Source.GRID,
        # ).exists()

    def test_csv_negative_consumption_raise_error_and_rollback(
        self, invalid_consumption_kwh_source_csv_file
    ):
        out = StringIO()

        with pytest.raises(
            ValidationError,
            match="Consumption Kwh must be a positive number.",
        ):
            call_command(
                "import_flow",
                invalid_consumption_kwh_source_csv_file,
                stdout=out,
            )

        # assert not Business.objects.filter(name="Business A").exists()
        # assert not Business.objects.filter(name="Business B").exists()
        # assert not EnergyConsumption.objects.filter(
        #     date="2023-07-15",
        #     consumption_kwh=-150.5,
        #     source=EnergyConsumption.Source.SOLAR,
        # ).exists()
        # assert not EnergyConsumption.objects.filter(
        #     date="2023-07-15",
        #     consumption_kwh=200.75,
        #     source="fire",
        # ).exists()
        # assert not EnergyConsumption.objects.filter(
        #     date="2023-07-16",
        #     consumption_kwh=160.3,
        #     source=EnergyConsumption.Source.GRID,
        # ).exists()
