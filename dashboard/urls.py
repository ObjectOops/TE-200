from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="dashboard_index"),
    path("instructor/", views.instructor_dashboard, name="instructor_dashboard"),
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("instructor/create_class", views.create_class, name="create_class"),
    path("student/join_class", views.join_class, name="join_class")
]
