from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from login.models import User

def index(request):
    return render(request, "student/index.html", {})
