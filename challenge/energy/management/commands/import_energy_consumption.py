import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from challenge.energy.models import Business, EnergyConsumption


class Command(BaseCommand):
    help = "Import Business and Energy Consumptions from CSV file"
    required_columns: list[str] = [
        "business_name",
        "address",
        "contact_email",
        "date",
        "consumption_kwh",
        "source",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            type=str,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        businesses_cache = {}
        file = options["file"]

        if not Path(file).exists():
            raise CommandError('File "%s" not found' % file)

        with Path(file).open() as csvfile:
            reader = csv.DictReader(csvfile)

            content = list(reader)
            if not content:
                raise CommandError('File "%s" is empty' % file)

            actual_columns = reader.fieldnames
            if not actual_columns == self.required_columns:
                raise CommandError(
                    "The file does not have the correct columns or the correct order.\n"
                    f"Expected: {self.required_columns}\n"
                    f"Actual: {actual_columns}\n"
                )

            imported_consumptions = 0

            for row in content:
                if row["business_name"] not in businesses_cache:
                    business, _ = Business.objects.update_or_create(
                        name=row["business_name"],
                        address=row["address"],
                        contact_email=row["contact_email"],
                    )
                    businesses_cache[row["business_name"]] = business
                else:
                    business = businesses_cache[row["business_name"]]

                _, created = EnergyConsumption.objects.update_or_create(
                    date=row["date"],
                    consumption_kwh=float(row["consumption_kwh"]),
                    source=row["source"],
                    business=business,
                )
                if created:
                    imported_consumptions += 1

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully imported "%d" energy consumptions'
                    % imported_consumptions
                )
            )
