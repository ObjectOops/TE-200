from random import randint
from hashlib import sha256
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import Attendance

def index(request):
    return render(request, "main/index.html", {})

def instructor_dashboard(request):
    attendances = Attendance.objects.order_by("-opening")
    context = {"attendances": attendances}
    return render(request, "main/instructor.html", context)

def instructor_create(request):
    code = hex(randint(0x0, 0xFFFFFF))[2:]
    route_id = sha256(code.encode('utf-8')).hexdigest()[0:6]
    opening = timezone.now()
    closing = opening + timedelta(minutes=10)
    new_attendance = Attendance(route_id=route_id, opening=opening, closing=closing, code=code)
    new_attendance.save()
    return HttpResponseRedirect(reverse("instructor_detail", args=(new_attendance.route_id,)))

def instructor_detail(request, attendance_route):
    attendance_route_validate(attendance_route)
    attendance = Attendance.objects.get(route_id=attendance_route)
    context = {"attendance": attendance}
    return render(request, "main/instructor_detail.html", context)

def student_join(request):
    return render(request, "main/student.html", {})

def student_validate(request):
    joinCode = request.POST.get("joinCode")
    if joinCode is None:
        return HttpResponse("Invalid join code.")
    attendance = Attendance.objects.filter(code=joinCode).first()
    if attendance is None:
        return HttpResponse("Join code not found.")
    if not attendance.is_open():
        return HttpResponse("Attendance expired.")
    attendee_name = request.POST.get("attendeeName")
    if len(attendee_name) == 0:
        attendee_name = "Anonymous"
    attendance.add_attendee(attendee_name)
    return HttpResponseRedirect(reverse("student_detail", args=(attendance.route_id,)))

def student_detail(request, attendance_route):
    attendance_route_validate(attendance_route)
    attendance = Attendance.objects.get(route_id=attendance_route)
    context = {"attendance": attendance}
    return render(request, "main/student_detail.html", context)

def attendance_route_validate(route_id):
    get_object_or_404(Attendance, route_id=route_id)
