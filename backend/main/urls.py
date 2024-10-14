from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("instructor/create/", views.instructor_create, name="instructor create"),
    path("instructor/class/<int:attendance_id>/", views.instructor_detail, name="instructor detail"),
    path("student/join/", views.student_join, name="student join"),
    path("student/class/<int:attendance_id>/", views.student_detail, name="student detail")
]
