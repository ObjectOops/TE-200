import random
import hashlib
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.utils import timezone

from .models import AttendanceCode, AttendanceSession

def index(request):
    return render(request, "main/index.html", {})

def instructor_dashboard(request):
    attendances = AttendanceCode.objects.order_by("-opening")
    context = {"attendances": attendances}
    return render(request, "main/instructor.html", context)

def instructor_create(request):
    code = hex(random.randint(0x0, 0xFFFFFF))[2:]
    route_id = hashlib.sha256(code.encode('utf-8')).hexdigest()[0:6]
    new_class = AttendanceCode(code=code, route_id=route_id)
    new_class.save()
    opening = timezone.now()
    closing = opening + timedelta(minutes=10)
    new_session = new_class.attendancesession_set.create(opening=opening, closing=closing)
    new_class.sessions.insert(0, new_session.pk)
    new_class.save()
    new_session.save()
    return HttpResponseRedirect(reverse("instructor detail", args=(new_class.route_id,)))

def instructor_detail(request, attendance_route):
    attendance_route_validate(attendance_route)
    sessions = AttendanceCode.objects.get(route_id=attendance_route).attendancesession_set.all()
    context = {"sessions": sessions}
    return render(request, "main/instructor_detail.html", context)

def student_join(request):
    return HttpResponse("Student join.")

def student_detail(request, attendance_route):
    attendance_route_validate(attendance_route)
    return HttpResponse(f"Student detail attendance {attendance_route}.")

def student_validate(request):
    # if request.method != "POST":
    #     return HttpResponseNotAllowed(["POST"])
    # attendance_code = request.body
    # attendance = AttendanceCode.objects.filter(code=attendance_code).first()
    # if attendance is None or not attendance.is_open():
    #     return HttpResponse()
    # AttendanceSession.add_attendee(attendance.session_pk)
    # return HttpResponse(attendance.route_id)
    return HttpResponse("Placeholder")

def attendance_route_validate(route_id):
    get_object_or_404(AttendanceCode, route_id=route_id)
