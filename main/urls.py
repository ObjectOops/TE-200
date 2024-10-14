from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("instructor/", views.instructor_dashboard, name="instructor dashboard"),
    path("instructor/create/", views.instructor_create, name="instructor create"), # POST
    path("instructor/class/<str:attendance_route>/", views.instructor_detail, name="instructor detail"),
    path("student/join/", views.student_join, name="student join"),
    path("student/validate/", views.student_validate, name="student validate"), # POST
    path("student/class/<str:attendance_route>/", views.student_detail, name="student detail")
]
