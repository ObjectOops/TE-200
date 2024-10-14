from django.db import models
from django.utils import timezone
from datetime import timedelta

class AttendanceCode(models.Model):
    code = models.CharField(max_length=6)
    opening = models.DateTimeField("opening time")
    closing = models.DateTimeField("closing time")

    def __str__(self):
        return f"{self.code} | {self.opening} | {self.closing}"
    
    def is_open(self):
        now = timezone.now()
        return self.opening <= now and now < self.closing

class Attendance(models.Model):
    attendance_code = models.ForeignKey(AttendanceCode, on_delete=models.CASCADE)
    date_taken = models.DateTimeField("date taken")
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.attendance_code.code} | {self.count}"
