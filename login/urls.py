from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="login_index"),
    path("instructor/", views.instructor_login, name="instructor_login"),
    path("instructor/auth/", views.instructor_auth, name="instructor_auth"), # POST
    path("student/", views.student_login, name="student_login"),
    path("student/auth/", views.student_auth, name="student_auth"), # POST
    path("debug/", views.debug_interface, name="debug_interface"),
    path("debug/create_user", views.create_user, name="create_user")
]
