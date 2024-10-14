from django.contrib import admin

from .models import AttendanceCode, AttendanceSession

admin.site.register(AttendanceCode)
admin.site.register(AttendanceSession)
