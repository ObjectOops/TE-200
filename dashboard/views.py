from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from login.models import User
from util import SessionState

def index(request):
    session_state = SessionState(from_dict=request.session.get(
        "state", 
        SessionState().to_dict()
    ))
    if not session_state.signed_in:
        return HttpResponseRedirect(reverse("login_index"))
    if session_state.is_instructor:
        return HttpResponseRedirect(reverse("instructor_dashboard"))
    return HttpResponseRedirect(reverse("student_dashboard"))

def instructor_dashboard(request):
    return render(request, "dashboard/instructor.html")

def student_dashboard(request):
    return render(request, "dashboard/student.html")
