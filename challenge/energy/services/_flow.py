from django.db import transaction

from challenge.energy.models import MeterPoint

from ._base import AbstractFlow


class D0010002(AbstractFlow):
    """Imports Flow Reference: D0010, Flow Version: 002

    https://www.electralink.co.uk/data-catalogues/dtc-catalogue/
    """

    def __init__(self, content: str, file_name: str) -> None:
        super().__init__(content=content, file_name=file_name)

    @transaction.atomic
    def execute(self):
        """Parse the content of the flow (.uff) file"""
        lines = [
            [i for i in line.strip().split("|")]
            for line in self.content.split("\n")
            if line
        ]

        meter_point = 0
        for line in lines[1:]:
            # MPAN Cores
            if line[0] == "026":
                _, mpan, validation_status = line
                meter_point = MeterPoint.objects.update_or_create(
                    mpan=mpan, validation_status=validation_status
                )
                pass

            # Meter/Reading Types
            if line[0] == "028":
                pass

            # Register Readings
            if line[0] == "030":
                pass
