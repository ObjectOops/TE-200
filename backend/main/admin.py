from django.contrib import admin

from .models import AttendanceCode, Attendance

admin.site.register(AttendanceCode)
admin.site.register(Attendance)
