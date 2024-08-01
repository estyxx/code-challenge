from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class MeterPoint(models.Model):
    # Choices
    class ValidationStatus(models.TextChoices):
        FAILED = "F", _("Failed")
        NOT_VALIDATED = "U", _("Not validated")
        VALIDATED = "V", _("Validated")

    # Fields
    mpan = models.CharField(
        _("MPAN Core"),
        max_length=13,
        help_text=_(
            "The unique national reference for a Metering System or an Asset "
            "Metering System."
        ),
    )
    validation_status = models.CharField(
        verbose_name=_("Validation Status"),
        max_length=1,
        choices=ValidationStatus.choices,
        help_text=_(
            "Indicates whether readings or Half Hourly advances have been validated "
            "for BSC Settlement, passed BSC Validation or failed BSC Validation."
        ),
    )

    # Methods

    def __str__(self) -> str:
        return f"{self.mpan} | {self.validation_status}"

    def clean(self) -> None:
        super().clean()
        if self.validation_status not in self.ValidationStatus.values:
            raise ValidationError(
                {
                    "validation_status": _(
                        f"Invalid ValidationStatus: {self.validation_status}. "
                        "(Allowed: "
                        f"{', '.join([i.value for i in self.ValidationStatus])})"
                    )
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)


class Meter(models.Model):
    # Choices
    class ReadingType(models.TextChoices):
        A = "A", _("Actual Change of Supplier Read")
        C = "C", _("Customer own read")
        D = (
            "D",
            _("Deemed (Settlement Registers) or Estimated (Non-Settlement Registers)"),
        )
        F = "F", _("Final")
        I = "I", _("Initial")
        M = "M", _("MAR")
        O = "O", _("Old Supplier's Estimated CoS Reading")
        P = "P", _("Electronically collected via PPMIP")
        Q = "Q", _("Meter Reading modified manually by DC")
        R = "R", _("Routine")
        S = "S", _("Special")
        T = "T", _("Proving Test Reading")
        U = "U", _("Forward Migration CoA")
        V = "V", _("Forward Migration CoS")
        W = "W", _("Withdrawn")
        X = "X", _("Supplier Agreed Switch Read")
        Y = "Y", _("Reverse Migration CoS")
        Z = "Z", _("Actual Change of Tenancy Read")

    # Fields
    meter_id = models.CharField(
        _("Meter Id (Serial Number)"),
        max_length=10,
        help_text=_(
            "The serial number which is stamped onto the meter nameplate at "
            "manufacture, which is used as the main identifier of a Meter."
        ),
    )
    reading_type = models.CharField(
        verbose_name=_("Rading Type"),
        max_length=1,
        choices=ReadingType.choices,
        help_text=_("A code identifying the type of reading."),
    )

    # Foreign Keys

    meter_point = models.ForeignKey(
        MeterPoint,
        verbose_name=_("Meter Point"),
        on_delete=models.CASCADE,
        related_name="meters",
    )

    # Methods
    def __str__(self) -> str:
        return f"{self.meter_id} {self.reading_type} ({self.meter_point})"

    def clean(self) -> None:
        super().clean()
        if self.reading_type not in self.ReadingType.values:
            raise ValidationError(
                {
                    "reading_type": _(
                        f"Invalid ReadingType: {self.reading_type}. (Allowed: {', '.join([i.value for i in self.ReadingType])})"
                    )
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)


class Reading(models.Model):
    # Choices
    class Flag(models.TextChoices):
        VALID = "T", _("Valid")
        SUSPECT = "F", _("Suspect")

    class Method(models.TextChoices):
        N = "N", _("Not viewed by an Agent or Non Site Visit")
        P = "P", _("Viewed by an Agent or Site Visit")

    # Fields
    meter_register_id = models.CharField(
        _("Meter Register Id"),
        max_length=2,
        help_text=_("The reference Id for a Meter Register within a meter."),
    )
    reading_at = models.DateTimeField(
        _("Reading Date & Time"),
        help_text=_(
            "The date and time at which a meter register reading is taken. "
            "The time is always midnight for Non-Half Hourly readings with "
            "the exception of *special* reads where the absolute reading time "
            "must be given."
        ),
    )
    register_reading = models.DecimalField(
        _("Register Reading"),
        decimal_places=1,
        max_digits=10,
        help_text=_(
            "The value of a reading from a meter register at a specified date and time."
        ),
    )
    md_reset_at = models.DateTimeField(
        _("MD Reset Date & Time"),
        help_text=_(
            "The date and time at which a Maximum Demand Meter is reset to zero."
        ),
        null=True,
        blank=True,
    )
    md_resets_number = models.PositiveSmallIntegerField(
        _("Number of MD Resets"),
        help_text=_(
            "The number of times that the Maximum Demand Indicator has been reset."
        ),
    )
    meter_reading_flag = models.CharField(
        _("Meter Reading Flag"),
        choices=Flag.choices,
        max_length=1,
        help_text=_("Indicates whether register reading is valid or suspect."),
    )
    reading_method = models.CharField(
        _("Reading Method"),
        choices=Method.choices,
        max_length=1,
        help_text=_("Indicates how the meter reading was obtained"),
    )

    # TODO: add ForeignKey with ImportFlowFiles table
    flow_file = models.CharField(
        verbose_name=_("Flow File"),
        max_length=100,
        help_text=_("The filename of the flow file that the reading came in"),
    )

    # Foreign Keys

    meter = models.ForeignKey(
        Meter,
        verbose_name=_("Meter"),
        on_delete=models.CASCADE,
        related_name="readings",
    )
    meter_point = models.ForeignKey(
        MeterPoint,
        verbose_name=_("Meter Point"),
        on_delete=models.CASCADE,
        related_name="readings",
    )

    # Methods
    def __str__(self) -> str:
        return f"{self.reading_at} ({self.meter.meter_id}) {self.register_reading}"

    def clean(self) -> None:
        super().clean()
        if self.meter_reading_flag not in self.Flag.values:
            raise ValidationError(
                {
                    "reading_type": _(
                        f"Invalid Flag: {self.meter_reading_flag}. (Allowed: {', '.join([i.value for i in self.Flag])})"
                    )
                }
            )

        if self.reading_method not in self.Method.values:
            raise ValidationError(
                {
                    "reading_type": _(
                        f"Invalid Method: {self.reading_method}. (Allowed: {', '.join([i.value for i in self.Method])})"
                    )
                }
            )

        if self.register_reading < 0:
            raise ValidationError(
                {"register_reading": _("Register reading must be a positive number.")}
            )

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)


class FlowImportFiles(models.Model):
    # TODO: add header and footer fields that are in the files for convenience?
    imported_at = models.DateTimeField(
        _("Import Date & Time"),
        help_text=_("The date and time at which a file has been imported"),
        auto_now_add=True,
    )
    name = models.CharField(
        _("File name"), max_length=50, help_text=_("Name of the .uff file")
    )
    # TODO: move to an S3 bucket if it's too big to keep in the database!
    content = models.TextField(
        _("File Content"), help_text=_("Content of the imported file")
    )

    successful = models.BooleanField(_("Successful import flag"), default=False)

    def mark_flow_succesful(self) -> None:
        self.successful = True
        self.save()
