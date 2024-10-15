from django.db import models
from django.utils import timezone
from datetime import timedelta

class AttendanceCode(models.Model):
    code = models.CharField(max_length=6)
    route_id = models.CharField(max_length=6)
    sessions = models.JSONField(default=list)

    def __str__(self):
        return f"{self.code} | {self.get_session().pk if self.get_session() is not None else "ERROR"}"
        
    def get_session(self):
        if len(self.sessions) > 0:
            return AttendanceSession.objects.filter(pk=self.sessions[-1]).first()
        return None

class AttendanceSession(models.Model):
    attendance_code = models.ForeignKey(AttendanceCode, on_delete=models.CASCADE)
    opening = models.DateTimeField()
    closing = models.DateTimeField()
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.attendance_code.code} | {self.count}"

    def is_open(self):
        now = timezone.now()
        return self.opening <= now and now < self.closing
