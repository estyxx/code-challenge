# code-challenge

Personal repo to practice interview code challenges

## Problem

**Django Backend Challenge: Energy Consumption CSV Loader**

**Overview:**

You are tasked with building a Django management command to import energy consumption data from a CSV file into the database. The command should ensure idempotency, meaning running the command multiple times with the same data should not create duplicate records. Additionally, the operation should be atomic, ensuring data integrity even if an error occurs during the process.

**Requirements:**

1. **Data Model:**

   Create the following Django models:

   - **Business:** Represents a business entity.
     - Fields: `name` (CharField), `address` (CharField), `contact_email` (EmailField)
   - **EnergyConsumption:** Represents energy consumption data.
     - Fields: `business` (ForeignKey to Business), `date` (DateField), `consumption_kwh` (FloatField), `source` (CharField, choices=[('solar', 'Solar'), ('wind', 'Wind'), ('grid', 'Grid')])
     - Constraints: Ensure that `business`, `date`, and `source` are unique together.

2. **CSV Format:**

   The CSV file will have the following columns:

   - `business_name`: The name of the business (string)
   - `address`: The address of the business (string)
   - `contact_email`: The contact email of the business (string)
   - `date`: The date of energy consumption (YYYY-MM-DD format)
   - `consumption_kwh`: The amount of energy consumed in kWh (float)
   - `source`: The source of energy (solar, wind, or grid)

3. **Management Command:**

   Implement a Django management command that does the following:

   - Reads the CSV file.
   - Creates or updates `Business` and `EnergyConsumption` records based on the data in the CSV.
   - Ensures idempotency (i.e., running the command multiple times with the same data should not create duplicate records).
   - Uses atomic transactions to ensure that the entire operation is rolled back if an error occurs.

4. **Validation and Error Handling:**

   - Validate the data in the CSV file (e.g., correct date format, valid energy source).
   - Handle cases where the business data in the CSV does not match any existing records.

5. **Testing:**

   - Write unit tests for your models and the management command using Django's testing framework.

**Hints and Tips:**

- Use the `get_or_create` method to handle idempotency for the `Business` model.
- Use unique constraints and the `update_or_create` method to handle idempotency for the `EnergyConsumption` model.
- Use the `transaction.atomic` decorator to ensure atomic operations.
- Consider edge cases, such as malformed CSV data or partial updates.

**Example Usage:**

```bash
python manage.py import_energy_consumption /path/to/your/csvfile.csv
```

**Sample CSV Data:**

```csv
business_name,address,contact_email,date,consumption_kwh,source
Business A,123 Business St,businessa@example.com,2023-07-15,150.5,solar
Business B,456 Enterprise Rd,businessb@example.com,2023-07-15,200.75,wind
Business A,123 Business St,businessa@example.com,2023-07-16,160.3,grid
```

**Submission:**

- Provide a link to a public repository (e.g., GitHub) with your complete Django project.
- Include a README file with instructions on how to set up and run your project locally, as well as how to run the tests.

## Quick start

Install the dependencies

    poetry install

### Create superuser

To create a superuser account, use this command:

    poetry run python manage.py createsuperuser

### Running tests

    pytest
