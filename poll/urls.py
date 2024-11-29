from django.urls import path

from . import views

urlpatterns = [
    path("create_poll/<str:class_route_id>/", views.create_poll, name="create_poll"),
    path("<str:class_route_id>/<str:poll_route_id>", views.poll_detail, name="poll_detail"),
    path("answer_poll/<str:class_route_id>/", views.answer_poll, name="answer_poll")
]
