import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory

from challenge.tasks.models import Task
from challenge.tasks.views import TaskList

pytestmark = pytest.mark.django_db


def test_get():
    factory = APIRequestFactory()
    request = factory.post("/tasks/", {"title": "new idea"}, format="json")
    view = TaskList.as_view()
    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {
        "id": 1,
        "title": "new idea",
        "description": "",
        "status": "pending",
        "priority": None,
        "due_date": None,
    }
    assert Task.objects.filter(id=1).exists()
