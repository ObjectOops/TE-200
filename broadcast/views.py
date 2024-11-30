import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from dotenv import load_dotenv

from dashboard.models import ClassSession
from util import check_session, log_request

load_dotenv()
signaling_server_url = os.environ.get("SIGNALING_SERVER_URL")
print(f"Signaling Server URL: {signaling_server_url}")

def general_broadcast(instructor_only, template, request, route_id):
    redir, redir_name = check_session(request, instructor_only=instructor_only, allow_guest=True)
    if redir:
        return HttpResponseRedirect(reverse(redir_name))
    # I just realized that this operation can be replaced by one of Django's utility functions.
    class_session = ClassSession.objects.filter(route_id=route_id).first()
    if class_session is None:
        return HttpResponse(status=404)
    return render(request, template, {
        "class": class_session,
        "signaling_server_url": signaling_server_url
    })

def instructor_broadcast(request, route_id):
    log_request(request)
    return general_broadcast(True, "broadcast/instructor.html", request, route_id)

def student_broadcast(request, route_id):
    log_request(request)
    return general_broadcast(False, "broadcast/student.html", request, route_id)
