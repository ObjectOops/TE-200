from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("instructor/", views.instructor_dashboard, name="instructor_dashboard"),
    path("instructor/create/", views.instructor_create, name="instructor_create"), # POST
    path("instructor/attendance/<str:attendance_route>/", views.instructor_detail, name="instructor_detail"),
    path("student/join/", views.student_join, name="student_join"),
    path("student/validate/", views.student_validate, name="student_validate"), # POST
    path("student/attendance/<str:attendance_route>/", views.student_detail, name="student_detail")
]
