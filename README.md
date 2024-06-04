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

### **Objective:**

Create a Django-based RESTful API for managing tasks. The API should support the creation, retrieval, updating, and deletion of tasks. Each task should have a title, description, status, priority, and due date. Additionally, implement an endpoint that provides a summary of tasks based on their status.

### **Requirements:**

1. **Models:**
   - Task
     - `title` (CharField)
     - `description` (TextField)
     - `status` (CharField: choices=['Pending', 'In Progress', 'Completed'])
     - `priority` (IntegerField: choices=1 to 5)
     - `due_date` (DateField)
2. **API Endpoints:**
   - `POST /tasks/` - Create a new task
   - `GET /tasks/` - Retrieve all tasks
   - `GET /tasks/<id>/` - Retrieve a single task by ID
   - `PUT /tasks/<id>/` - Update a task by ID
   - `DELETE /tasks/<id>/` - Delete a task by ID
   - `GET /tasks/summary/` - Retrieve a summary of tasks by status (e.g., number of tasks in 'Pending', 'In Progress', and 'Completed' status)
3. **Validation:**
   - Ensure that the `title` is unique.
   - Ensure that `priority` is between 1 and 5.
4. **Testing:**
   - Write unit tests for all endpoints.
   - Use Django’s test framework to ensure the correctness of the API.

### **Bonus Points:**

- Implement filtering by status, priority, and due date.
- Implement pagination for the list of tasks.
- Add a feature to search tasks by title or description.
- Ensure the API follows best practices for RESTful design.

### **Instructions:**

1. **Setup:**
   - Initialize a new Django project and app.
   - Use Django REST Framework (DRF) for building the API.
   - Configure SQLite as the database.
2. **Development:**
   - Define the `Task` model with the required fields and validations.
   - Create serializers for the `Task` model.
   - Implement views and URL routing for the API endpoints.
   - Add necessary validations and error handling.
3. **Testing:**
   - Write unit tests for each endpoint using Django’s test framework.
   - Ensure the tests cover various edge cases and invalid inputs.
4. **Documentation:**
   - Document the API endpoints and how to use them.
   - Include instructions on how to set up and run the project locally.

### **Expected Outcome:**

A Django project with a fully functional RESTful API for managing tasks, including the ability to create, retrieve, update, delete, and summarize tasks. The code should be clean, well-documented, and include comprehensive unit tests.

### **Submission:**

Submit your code as a GitHub repository or a zip file with the complete project. Ensure the README file contains setup instructions and API documentation.
