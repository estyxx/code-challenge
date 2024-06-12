# Generated by Django 5.0.6 on 2024-06-12 15:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnergyConsumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumption', models.IntegerField(help_text=' Energy consumed in kWh', verbose_name='Consumption')),
                ('timestamp', models.DateTimeField(help_text='DateTime of the energy consumption record', verbose_name='Timestamp')),
                ('source', models.CharField(choices=[('solar', 'Solar'), ('wind', 'Wind'), ('grid', 'Grid')], help_text='Source of the energy', max_length=10, verbose_name='Source')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Energy Consumption',
                'verbose_name_plural': 'Energy Consumptions',
                'unique_together': {('timestamp', 'uploaded_by')},
            },
        ),
    ]