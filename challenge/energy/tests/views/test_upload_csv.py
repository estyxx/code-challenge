from datetime import datetime
from typing import TYPE_CHECKING

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

from challenge.energy.models import EnergyConsumption
from challenge.users.models import User

if TYPE_CHECKING:
    from challenge.energy.tests.factories import EnergyConsumptionFactory
    from challenge.users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_user_is_authenticated_happy_path(client: Client, user: User) -> None:
    client.force_login(user)
    csv_content = b"timestamp,consumption,source\n2024-06-12T00:00:00,12100,solar"
    csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")

    response = client.post(reverse("upload_csv"), {"file": csv_file})

    assert response.status_code == 302
    assert response.url == reverse("upload_success")
    assert EnergyConsumption.objects.filter(
        uploaded_by=user, timestamp=datetime(2024, 6, 12, 0, 0, 0)
    ).exists()
    obj = EnergyConsumption.objects.get(
        uploaded_by=user, timestamp=datetime(2024, 6, 12, 0, 0, 0)
    )
    assert obj.source == EnergyConsumption.Source.SOLAR


def test_upload_batch_consumptions(client: Client, user: User) -> None:
    client.force_login(user)
    csv_content = (
        "timestamp,consumption,source\n"
        "2024-06-11T00:00:00,12100,solar\n"
        "2024-02-12T00:00:00,11100,wind"
    )
    csv_file = SimpleUploadedFile(
        "test.csv", csv_content.encode("utf-8"), content_type="text/csv"
    )

    response = client.post(reverse("upload_csv"), {"file": csv_file})

    assert response.status_code == 302
    assert response.url == reverse("upload_success")
    assert (
        EnergyConsumption.objects.filter(
            uploaded_by=user,
        ).count()
        == 2
    )
    obj1 = EnergyConsumption.objects.get(
        uploaded_by=user, timestamp=datetime(2024, 6, 11, 0, 0, 0)
    )
    assert obj1.source == EnergyConsumption.Source.SOLAR
    obj2 = EnergyConsumption.objects.get(
        uploaded_by=user, timestamp=datetime(2024, 2, 12, 0, 0, 0)
    )
    assert obj2.source == EnergyConsumption.Source.WIND


def test_user_is_not_authenticated_redirect(client: Client) -> None:
    csv_content = b"timestamp,consumption,source\n2024-06-12T00:00:00,100.5,solar"
    csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")

    response = client.post(reverse("upload_csv"), {"file": csv_file})

    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/energy/upload-csv/"


def test_upload_empty_file_return_error(client: Client, user: User) -> None:
    client.force_login(user)
    csv_file = SimpleUploadedFile("empty.csv", b"", content_type="text/csv")

    response = client.post(reverse("upload_csv"), {"file": csv_file})

    assert response.status_code == 200
    assert "The submitted file is empty." in response.context["form"].errors["file"]


def test_upload_with_no_file_return_error(client: Client, user: User) -> None:
    client.force_login(user)

    response = client.post(reverse("upload_csv"), {})

    assert response.status_code == 200
    assert "This field is required." in response.context["form"].errors["file"]


def test_file_with_title_row_only(client: Client, user: User) -> None:
    client.force_login(user)
    csv_content = b"timestamp,consumption,source\n"
    csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")

    response = client.post(reverse("upload_csv"), {"file": csv_file})

    assert response.status_code == 200
    assert (
        "The CSV file is missing the values rows."
        in response.context["form"].errors["file"]
    )


def test_row_already_processed_raise_error(
    client: Client,
    user_factory: "UserFactory",
    energy_consumption_factory: "EnergyConsumptionFactory",
) -> None:
    user = user_factory(email="energy@ester.it")
    consumption = energy_consumption_factory(
        uploaded_by=user,
    )
    client.force_login(user)
    csv_content = (
        "timestamp,consumption,source\n"
        f"{consumption.timestamp},{consumption.consumption},{consumption.source[0]}"
    )
    csv_file = SimpleUploadedFile(
        "test.csv", csv_content.encode("utf-8"), content_type="text/csv"
    )

    response = client.post(reverse("upload_csv"), {"file": csv_file})

    assert response.status_code == 200
    assert (
        "Row 1 it's already on the system" in response.context["form"].errors["file"][0]
    )


def test_upload_identical_consumptions(client: Client, user: User) -> None:
    client.force_login(user)
    csv_content = (
        "timestamp,consumption,source\n"
        "2024-06-11T00:00:00,12100,solar\n"
        "2024-06-11T00:00:00,12100,solar\n"
        "2024-02-12T00:00:00,11100,wind"
    )
    csv_file = SimpleUploadedFile(
        "test.csv", csv_content.encode("utf-8"), content_type="text/csv"
    )

    response = client.post(reverse("upload_csv"), {"file": csv_file})

    assert response.status_code == 200
    assert (
        "Row 2 it's already on the system" in response.context["form"].errors["file"][0]
    )
    assert (
        EnergyConsumption.objects.filter(
            uploaded_by=user,
        ).count()
        == 0
    )
