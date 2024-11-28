from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from login.models import User
from util import SessionState, sha256_hash

def index(request):
    return render(request, "login/index.html", {})

def instructor_login(request):
    return render(request, "login/instructor.html", {})

def instructor_auth(request):
    user = auth_challenge(request)
    if user is not None and user.is_instructor:
        session = request.session
        session["state"] = SessionState(signed_in=True, is_instructor=True).to_dict()
        session["username"] = user.username
        return HttpResponseRedirect(reverse("instructor_dashboard", current_app="dashboard"))
    return render(request, "login/instructor.html", {"banner_msg": "Invalid login."})

def student_login(request):
    return render(request, "login/student.html")

def student_auth(request):
    user = auth_challenge(request)
    if user is not None:
        session = request.session
        session["state"] = SessionState(signed_in=True, is_instructor=False).to_dict()
        session["username"] = user.username
        return HttpResponseRedirect(reverse("student_dashboard", current_app="dashboard"))
    return render(request, "login/student.html", {"banner_msg": "Invalid login."})

def auth_challenge(request):
    form = request.POST
    username = form.get("username")
    password = form.get("password")
    user = User.objects.filter(username=username).first()
    if user is None:
        return None
    authenticated = user.authenticate(password)
    if not authenticated:
        return None
    return user

def debug_interface(request):
    return render(request, "login/debug.html", {})

def create_user(request):
    form = request.POST
    username = form.get("username")
    password = form.get("password")
    is_instructor = form.get("is-instructor") == "true"
    new_user = User(
        username=username, 
        hash_sha256=sha256_hash(password), 
        is_instructor=is_instructor
    )
    new_user.save()
    return render(request, "login/debug.html", {})
