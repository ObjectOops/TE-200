from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from login.models import User

def index(request):
    return render(request, "login/index.html", {})

def instructor_login(request):
    return render(request, "login/instructor.html", {})

def instructor_auth(request):
    user = auth_challenge(request)
    if user is not None and user.is_instructor:
        return HttpResponseRedirect(reverse("index", current_app="instructor"))
    context = {
        "banner": render(request, "login/banner.html", {
            "msg": "Invalid login."
        })
    }
    return render(request, "login/instructor.html", context)

def student_login(request):
    return render(request, "login/student.html")

def student_auth(request):
    user = auth_challenge(request)
    if user is not None:
        return HttpResponseRedirect(reverse("index", current_app="student"))
    context = {
        "banner": render(request, "login/banner.html", {
            "msg": "Invalid login."
        })
    }
    return render(request, "login/student.html", context)

def auth_challenge(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username is None or password is None:
        return None
    user = User.objects.filter(username=username).first()
    if user is None:
        return None
    authenticated = user.authenticate(password)
    if not authenticated:
        return None
    return user
