from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="class_index"),
    path("join/", views.guest_join, name="guest_join"),
    path("<str:route_id>/instructor/", views.instructor_class, name="instructor_class"),
    path("<str:route_id>/student/", views.student_class, name="student_class")
]
