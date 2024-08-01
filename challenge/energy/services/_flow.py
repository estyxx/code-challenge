import datetime

from django.db import transaction

from challenge.energy.models import Meter, MeterPoint, Reading

from ._base import AbstractFlow
from ._exceptions import InvalidFormatError


class D0010002(AbstractFlow):
    """Imports Flow Reference: D0010, Flow Version: 002

    https://www.electralink.co.uk/data-catalogues/dtc-catalogue/
    """

    def __init__(self, content: str, file_name: str) -> None:
        super().__init__(content=content, file_name=file_name)

    @transaction.atomic
    def execute(self):
        """Parse the content of the flow (.uff) file"""

        # TODO: move import logging in a decorator
        import_file = self.log_import()

        # The `line[:-1] is to remove the last "|" that otherwise `
        # would have add an empty field that doesn't exists...
        lines = [
            [i for i in line[:-1].strip().split("|")]
            for line in self.content.split("\n")
            if line
        ]

        meter_point = None
        meter = None
        for line in lines[1:]:
            try:
                # MPAN Cores
                if line[0] == "026":
                    # Every time we encounter a 026 line we reset the meter_point
                    # and meter
                    meter_point = None
                    meter = None

                    _, mpan, validation_status = line
                    meter_point, _ = MeterPoint.objects.update_or_create(
                        mpan=mpan, validation_status=validation_status
                    )
                    pass

                # Meter/Reading Types
                if line[0] == "028":
                    if not meter_point:
                        raise InvalidFormatError(
                            "The Meter/Reading line (028) is not following a MPAN (026) line"
                        )

                    _, meter_id, reading_type = line
                    meter, _ = Meter.objects.update_or_create(
                        meter_id=meter_id,
                        reading_type=reading_type,
                        meter_point=meter_point,
                    )

                # Register Readings
                if line[0] == "030":
                    if not meter_point:
                        raise InvalidFormatError(
                            "The Register Readings line (030) is not following a MPAN (026) line or 028 line"
                        )

                    (
                        _,
                        register_id,
                        read_at,
                        register_reading,
                        md_reset_at,
                        md_resets_number,
                        flag,
                        method,
                    ) = line

                    # TODO: chcek DateTimeField Reading.reading_at received a naive datetime (2016-03-01 00:00:00) while time zone support is active.
                    parsed_read_at = datetime.datetime.strptime(
                        read_at,
                        "%Y%m%d%H%M%S",
                    )
                    parsed_md_reset_at = (
                        datetime.datetime.strptime(md_reset_at, "%Y%m%d%H%M%S")
                        if md_reset_at
                        else None
                    )

                    Reading.objects.update_or_create(
                        meter_register_id=register_id,
                        meter_point=meter_point,
                        meter=meter,
                        reading_at=parsed_read_at,
                        register_reading=float(register_reading),
                        md_reset_at=parsed_md_reset_at,
                        md_resets_number=md_resets_number if md_resets_number else 0,
                        meter_reading_flag=flag,
                        reading_method=method,
                        flow_file=self.file_name,
                    )

            except IndexError:
                InvalidFormatError("The file is not in the expected format")

        import_file.mark_flow_succesful()
