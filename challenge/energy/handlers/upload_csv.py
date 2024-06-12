import csv
from typing import TYPE_CHECKING

from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from challenge.energy.exceptions import ConsumptionAlreadyProcessedError, EmptyFileError
from challenge.energy.models import EnergyConsumption

if TYPE_CHECKING:
    from challenge.users.models import User


class UploadCSVHandler:
    """Handles the Upload of the CSV file for the Energy Consumptions"""

    def __init__(self, file: UploadedFile, user: "User"):
        self.file = file
        self.user = user

    def __call__(self) -> None:
        with transaction.atomic():
            self.execute()

    def execute(self) -> None:
        decoded_file = self.file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        for index, row in enumerate(reader):
            if EnergyConsumption.objects.filter(
                uploaded_by=self.user, timestamp=row["timestamp"]
            ).exists():
                # Using index+1 to count the Title row as well
                raise ConsumptionAlreadyProcessedError(
                    f"Row {index+1} it's already on the system ({row['timestamp']})."
                    "Abort."
                )

            EnergyConsumption.objects.create(
                timestamp=row["timestamp"],
                consumption=row["consumption"],
                source=row["source"],
                uploaded_by=self.user,
            )

        if reader.line_num <= 1:
            raise EmptyFileError("The CSV file is missing the values rows.")
