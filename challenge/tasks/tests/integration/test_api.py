import pytest
from django.urls import reverse
from rest_framework import status

from challenge.tasks.models import Task

pytestmark = pytest.mark.django_db


def test_create_task(api_client) -> None:
    data = {"title": "hello world"}

    response = api_client.post(reverse("tasks"), data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    task = Task.objects.get(title="hello world")
    assert task.status == Task.Status.PENDING


def test_create_duplicate_task(api_client, task_factory) -> None:
    task_factory(title="duplicate")
    data = {"title": "duplicate"}

    response = api_client.post(reverse("tasks"), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"title": ["task with this Title already exists."]}


def test_create_wrong_priority(api_client) -> None:
    data = {"title": "Priority", "priority": "******"}

    response = api_client.post(reverse("tasks"), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"priority": ['"******" is not a valid choice.']}


def test_create_wrong_status(api_client) -> None:
    data = {"title": "Priority", "status": "custom"}

    response = api_client.post(reverse("tasks"), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"status": ['"custom" is not a valid choice.']}


def test_get_all_tesks(api_client, task_factory) -> None:
    task1 = task_factory(title="Task1")
    task2 = task_factory(title="Task2")

    response = api_client.get(reverse("tasks"), format="json")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data == [
        {
            "id": 1,
            "title": "Task1",
            "description": task1.description,
            "priority": task1.priority.value,
            "status": task1.status.value,
            "due_date": task1.due_date.strftime("%Y-%m-%d"),
        },
        {
            "id": 2,
            "title": "Task2",
            "description": task2.description,
            "priority": task2.priority.value,
            "status": task2.status.value,
            "due_date": task2.due_date.strftime("%Y-%m-%d"),
        },
    ]


def test_get_task(api_client, task) -> None:
    url = reverse("task_detail", kwargs={"pk": task.id})

    response = api_client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority.value,
        "status": task.status.value,
        "due_date": task.due_date.strftime("%Y-%m-%d"),
    }


def test_put_task(api_client, task) -> None:
    url = reverse("task_detail", kwargs={"pk": task.id})
    new_data = {"title": "my new fancy title"}

    response = api_client.put(url, data=new_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": task.id,
        "title": new_data["title"],
        "description": task.description,
        "priority": task.priority.value,
        "status": task.status.value,
        "due_date": task.due_date.strftime("%Y-%m-%d"),
    }
    assert Task.objects.get(id=task.id).title == new_data["title"]


def test_put_task_with_title_already_taken(api_client, task_factory) -> None:
    task_factory(title="Duplex")
    task_to_update = task_factory()

    url = reverse("task_detail", kwargs={"pk": task_to_update.id})
    new_data = {"title": "Duplex"}

    response = api_client.put(url, data=new_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"title": ["task with this Title already exists."]}


def test_delete_task(api_client, task) -> None:
    url = reverse("task_detail", kwargs={"pk": task.id})

    response = api_client.delete(url, format="json")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_summary(api_client, task_factory) -> None:
    task_factory(status=Task.Status.PENDING)
    task_factory(status=Task.Status.COMPLETED)
    task_factory(status=Task.Status.COMPLETED)
    task_factory(status=Task.Status.IN_PROGRESS)
    task_factory(status=Task.Status.IN_PROGRESS)

    response = api_client.get(reverse("summary"), format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "completed": 0,
        "in_progress": 0,
        "pending": 0,
    }
