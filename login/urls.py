from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("instructor/", views.instructor_login, name="instructor_login"),
    path("instructor/auth/", views.instructor_auth, name="instructor_auth"), # POST
    path("student/", views.student_login, name="student_login"),
    path("student/auth/", views.student_auth, name="student_auth") # POST
]
