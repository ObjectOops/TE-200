from django.urls import path

from . import views

urlpatterns = [
    path("<str:route_id>/instructor/", views.instructor_broadcast, name="instructor_broadcast"),
    path("<str:route_id>/student/", views.student_broadcast, name="student_broadcast")
]
