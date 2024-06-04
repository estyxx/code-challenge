from django.db import models
from django.utils.translation import gettext as _


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        IN_PROGRESS = "in_progress", _("In Progress")
        COMPLETED = "completed", _("Completed")

    class Priority(models.IntegerChoices):
        ONE = 1, "★"
        TWO = 2, "★★"
        THREE = 3, "★★★"
        FOUR = 4, "★★★★"
        FIVE = 5, "★★★★★"

    title = models.CharField(_("Title"), max_length=255, unique=True)
    description = models.TextField(_("Description"), blank=True)
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
    )
    priority = models.IntegerField(_("Priority"), choices=Priority.choices, null=True)
    due_date = models.DateField(_("Due date"), blank=True, null=True)
