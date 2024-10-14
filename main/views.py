from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.template import loader

from .models import AttendanceCode, AttendanceSession

def index(request):
    return render(request, "main/index.html", {})

def instructor_dashboard(request):
    attendances = AttendanceCode.objects.order_by("-opening")
    context = {"attendances": attendances}
    return render(request, "main/instructor.html", context)

def instructor_create(request):
    return HttpResponse("Instructor create.")

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
