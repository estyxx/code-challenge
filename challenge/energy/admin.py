from django.contrib import admin

from challenge.energy.models import Meter, MeterPoint, Reading


@admin.register(MeterPoint)
class MeterPointAdmin(admin.ModelAdmin):
    list_display = [
        "mpan",
        "validation_status",
    ]

    search_fields = [
        "mpan",
    ]


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ["meter_id", "reading_type", "meter_point"]
    search_fields = [
        "meter_point__mpan",
    ]


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    search_fields = [
        "meter__meter_point__mpan",
    ]
    list_display = [
        "meter_register_id",
        "reading_at",
        "register_reading",
        "reading_method",
    ]
