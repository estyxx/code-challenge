from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class EnergyConsumption(models.Model):
    class Source(models.TextChoices):
        SOLAR = "solar", _("Solar")
        WIND = "wind", _("Wind")
        GRID = "grid", _("Grid")

    consumption = models.IntegerField(
        verbose_name=_("Consumption"), help_text=_(" Energy consumed in kWh")
    )
    timestamp = models.DateTimeField(
        verbose_name=_("Timestamp"),
        help_text=_("DateTime of the energy consumption record"),
    )
    source = models.CharField(
        verbose_name=_("Source"),
        max_length=10,
        choices=Source.choices,
        help_text=_("Source of the energy"),
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consumptions",
    )

    class Meta:
        unique_together = ["timestamp", "uploaded_by"]
        verbose_name = _("Energy Consumption")
        verbose_name_plural = _("Energy Consumptions")

    def __str__(self) -> str:
        return f"{self.timestamp} - {self.consumption} ({self.source})"
