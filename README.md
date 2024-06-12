# code-challenge

Personal repo to practice interview code challenges

## Quick start

Install the dependencies

    poetry install

### Create superuser

To create a superuser account, use this command:

    poetry run python manage.py createsuperuser

### Running tests

    pytest

## Code Challenge: Energy Consumption Analysis and Optimization

### Background

In the effort to promote sustainability and reduce carbon footprints, analyzing and optimizing energy consumption is crucial. As part of a tech-for-good initiative in the energy sector, your task is to build a Django application that allows users to upload energy consumption data, analyze it, and provide optimization recommendations.

### Objective

Create a Django application that enables users to:

1. Upload energy consumption data.
2. View summary statistics of their energy usage.
3. Get recommendations on how to optimize their energy consumption to reduce waste and improve efficiency.

### Requirements

#### Part 1: Data Upload and Storage

1. Create a Django model `EnergyConsumption` to store the energy data. The model should include fields for:

   - `timestamp`: DateTime of the energy consumption record.
   - `consumption`: Energy consumed in kWh.
   - `source`: Source of the energy (e.g., solar, wind, grid).

2. Implement a view to upload a CSV file containing energy consumption data. The CSV file will have the following columns: `timestamp`, `consumption`, and `source`.

#### Part 2: Data Analysis

3. Create a view that displays the following summary statistics:

   - Total energy consumption.
   - Average daily consumption.
   - Peak consumption time and value.
   - Distribution of energy sources.

4. Implement a method to calculate and display recommendations based on the data. Recommendations should include:
   - Suggestions to shift energy usage to non-peak times.
   - Recommendations for increasing the use of renewable energy sources if applicable.
   - Identify any anomalous spikes in energy consumption.

#### Part 3: User Interface

5. Use Django templates to create a simple, user-friendly interface for:
   - Uploading the CSV file.
   - Viewing the summary statistics.
   - Displaying the recommendations.

##### Bonus Points

- Implement unit tests for your views and models.
- Use Django REST Framework to create an API endpoint for uploading data and retrieving statistics.
- Add a feature to visualize the consumption data using charts (e.g., line chart for energy consumption over time, pie chart for energy source distribution).

## Deliverables

- Django project with the required functionality.
- Clear instructions on how to set up and run the project.
- Sample CSV file for testing.
- Brief documentation explaining your approach and any assumptions made.

#### Evaluation Criteria

- Code quality and best practices.
- Completeness of the functionality.
- User experience and interface design.
- Efficiency and accuracy of the analysis and recommendations.
- Bonus: Test coverage and additional features.

#### Instructions

1. Clone the provided GitHub repository [GitHub Repo URL].
2. Create a new branch for your work.
3. Implement the required features.
4. Submit a pull request with your solution.
5. Ensure your code is well-documented and includes instructions for setup and usage.

Good luck, and thank you for contributing to a sustainable future!
