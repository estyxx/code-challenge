from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Business(models.Model):
    name = models.CharField(_("Name"), max_length=150, blank=True)
    address = models.CharField(_("Address"), max_length=200, blank=True)
    contact_email = models.EmailField(_("Contact email"), blank=True, unique=True)

    def __str__(self) -> str:
        return self.name


class EnergyConsumption(models.Model):
    class Source(models.TextChoices):
        SOLAR = "solar", _("Solar")
        WIND = "wind", _("Wind")
        GRID = "grid", _("Grid")

    business = models.ForeignKey(
        "Business",
        on_delete=models.CASCADE,
        related_name="consumptions",
    )
    date = models.DateField(
        _("Date"),
        auto_now=False,
        auto_now_add=False,
    )
    consumption_kwh = models.FloatField(_("Consumption Kwh"))
    source = models.CharField(_("Source"), max_length=6, choices=Source)

    class Meta:
        unique_together = [["business", "date", "source"]]

    def __str__(self) -> str:
        return f"{self.business} {self.date} ({self.source})"

    def clean(self) -> None:
        super().clean()
        if self.source not in self.Source.values:
            raise ValidationError(
                {
                    "source": _("Invalid source: %(value)s") % {"value": self.source},
                }
            )

        if self.consumption_kwh <= 0:
            raise ValidationError(
                {"consumption_kwh": _("Consumption Kwh must be a positive number.")}
            )

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)
