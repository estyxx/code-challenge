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
def valid_uff_file():
    """Creates a CSV file with valid data."""
    content = (
        "ZHV|0000475656|D0010002|D|UDMS|X|MRCY|20160302153151||||OPER|\n"
        "026|1200023305967|V|\n"
        "028|F75A 00802|D|\n"
        "030|S|20160222000000|56311.0|||T|N|\n"
        "026|1900001059816|V|\n"
        "028|S95105287|C|\n"
        "030|TO|20160224000000|81641.0|||T|N|\n"
        "026|1200033197420|V|\n"
        "028|L85A 28596|C|\n"
        "030|S|20160226000000|68902.0|||T|N|\n"
        "026|1200031039874|V|\n"
        "028|S76A 13884|C|\n"
        "030|S|20160226000000|17393.0|||T|N|\n"
        "026|1591055549625|V|\n"
        "028|D03L80840|C|\n"
        "030|A1|20160301000000|50548.0|||T|N|\n"
        "026|2200031930792|V|\n"
        "028|S85D24767|C|\n"
        "030|01|20160301000000|20231.0|||T|N|\n"
        "030|02|20160301000000|64472.0|||T|N|\n"
        "026|1200022664056|V|\n"
        "028|D03A 09936|D|\n"
        "030|S|20160221000000|77766.0|||T|N|\n"
        "026|1900005260419|V|\n"
        "028|D0248417|D|\n"
        "030|TO|20160222000000|24802.0|||T|N|\n"
        "026|1013044353630|V|\n"
        "028|S82E042896|C|\n"
        "030|01|20160228000000|88285.0|||T|N|\n"
        "026|1900005281720|V|\n"
        "028|36933604|D|\n"
        "030|DY|20160222000000|80598.0|||T|N|\n"
        "030|NT|20160222000000|15549.0|||T|N|\n"
        "026|2000055433806|V|\n"
        "028|D13C01717|C|\n"
        "030|01|20160301000000|7242.0|||T|N|\n"
        "ZPT|0000475656|35||11|20160302154650|\n"
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
