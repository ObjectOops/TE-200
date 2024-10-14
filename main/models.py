from django.db import models
from django.utils import timezone
from datetime import timedelta

class AttendanceCode(models.Model):
    code = models.CharField(max_length=6)
    route_id = models.CharField(max_length=6)
    sessions = models.JSONField(default=list)
    opening = models.DateTimeField()
    closing = models.DateTimeField()

    def __str__(self):
        return f"{self.code} | {self.opening} | {self.closing} | {self.get_session()}"
    
    def is_open(self):
        now = timezone.now()
        return self.opening <= now and now < self.closing
    
    def get_session(self):
        if len(self.sessions) > 0:
            return self.sessions[0]
        return None

class AttendanceSession(models.Model):
    attendance_code = models.ForeignKey(AttendanceCode, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.attendance_code.code} | {self.count}"
