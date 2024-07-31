import os
import tempfile

import pytest


@pytest.fixture()
def temp_file():
    """Creates a generic temporary file."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()

    yield temp_file.name

    os.remove(temp_file.name)


@pytest.fixture()
def valid_csv_file():
    """Creates a CSV file with valid data."""
    content = (
        "business_name,address,contact_email,date,consumption_kwh,source\n"
        "Business A,123 Business St,businessa@example.com,2023-07-15,150.5,solar\n"
        "Business B,456 Enterprise Rd,businessb@example.com,2023-07-15,200.75,wind\n"
        "Business A,123 Business St,businessa@example.com,2023-07-16,160.3,grid\n"
    )
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", newline="")
    temp_file.write(content)
    temp_file.close()

    yield temp_file.name

    os.remove(temp_file.name)


@pytest.fixture()
def invalid_dates_csv_file():
    """Creates a CSV file with invalid date format in second/third row"""
    content = (
        "business_name,address,contact_email,date,consumption_kwh,source\n"
        "Business A,123 Business St,businessa@example.com,2023-07-15,150.5,solar\n"
        "Business B,456 Enterprise Rd,businessb@example.com,15-07-2023,200.75,wind\n"
        "Business A,123 Business St,businessa@example.com,2023-16-07,160.3,grid\n"
    )
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", newline="")
    temp_file.write(content)
    temp_file.close()

    yield temp_file.name

    os.remove(temp_file.name)


@pytest.fixture()
def invalid_source_csv_file():
    """Creates a CSV file with invalid Source in the second row"""
    content = (
        "business_name,address,contact_email,date,consumption_kwh,source\n"
        "Business A,123 Business St,businessa@example.com,2023-07-15,150.5,solar\n"
        "Business B,456 Enterprise Rd,businessb@example.com,2023-07-15,200.75,fire\n"
        "Business A,123 Business St,businessa@example.com,2023-07-16,160.3,grid\n"
    )
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", newline="")
    temp_file.write(content)
    temp_file.close()

    yield temp_file.name

    os.remove(temp_file.name)


@pytest.fixture()
def invalid_consumption_kwh_source_csv_file():
    """Creates a CSV file with invalid negative Consumption Kwh in first row"""
    content = (
        "business_name,address,contact_email,date,consumption_kwh,source\n"
        "Business A,123 Business St,businessa@example.com,2023-07-15,-150.5,solar\n"
        "Business B,456 Enterprise Rd,businessb@example.com,2023-07-15,200.75,wind\n"
        "Business A,123 Business St,businessa@example.com,2023-07-16,160.3,grid\n"
    )
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", newline="")
    temp_file.write(content)
    temp_file.close()

    yield temp_file.name

    os.remove(temp_file.name)


@pytest.fixture()
def empty_file():
    """Creates an empty file."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()

    yield temp_file.name

    os.remove(temp_file.name)


@pytest.fixture()
def header_only_file():
    """Creates a file with just the header."""
    content = "business_name,address,contact_email,date,consumption_kwh,source\n"
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", newline="")
    temp_file.write(content)
    temp_file.close()

    yield temp_file.name

    os.remove(temp_file.name)


@pytest.fixture()
def invalid_format_file():
    """Creates a CSV file with an incorrect format."""
    content = (
        "name,location,email,timestamp,usage,origin\n"
        "Business A,123 Business St,businessa@example.com,2023-07-15,150.5,solar\n"
        "Business B,456 Enterprise Rd,businessb@example.com,2023-07-15,200.75,wind\n"
    )
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", newline="")
    temp_file.write(content)
    temp_file.close()

    yield temp_file.name

    os.remove(temp_file.name)
