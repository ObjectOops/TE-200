from django.http import HttpResponse
from django.shortcuts import render

def instructor_class(request, route_id):
    return HttpResponse("IC")

def student_class(request, route_id):
    return HttpResponse("SC")
