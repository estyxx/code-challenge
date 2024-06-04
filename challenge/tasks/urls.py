from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from challenge.tasks import views

urlpatterns = [
    path("tasks/", views.TaskList.as_view(), name="tasks"),
    path("tasks/<int:pk>/", views.TaskDetail.as_view(), name="task_detail"),
    path("tasks/summary/", views.TaskSummary.as_view(), name="summary"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
