from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world!")

def instructor_create(request):
    return HttpResponse("Instructor create.")

def instructor_detail(request, attendance_id):
    return HttpResponse(f"Instructor detail attendance {attendance_id}.")

def student_join(request):
    return HttpResponse("Student join.")

def student_detail(request, attendance_id):
    return HttpResponse(f"Student detail attendance {attendance_id}.")
