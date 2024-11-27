from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="dashboard_index"),
    path("instructor/", views.instructor_dashboard, name="instructor_dashboard"),
    path("student/", views.student_dashboard, name="student_dashboard")
]
