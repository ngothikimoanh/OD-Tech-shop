from django.urls import path

from manager import views

urlpatterns = [
    path("", views.employee_list_view, name="manager_employees_list"),
    path("create/", views.employee_create_view, name="manager_employees_create"),
]
