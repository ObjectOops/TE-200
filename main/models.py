from django.db import models
from django.utils import timezone
from django.db.models import F

class Attendance(models.Model):
    route_id = models.CharField(max_length=6)
    opening = models.DateTimeField()
    closing = models.DateTimeField()
    code = models.CharField(max_length=6)
    count = models.IntegerField(default=0)
    attendees = models.JSONField(default=list)

    def __str__(self):
        return " | ".join((self.route_id, str(self.opening), str(self.closing), self.code, str(self.count)))

    def is_open(self):
        now = timezone.now()
        return self.opening <= now and now < self.closing
    
    def add_attendee(self, attendee_name):
        self.count = F("count") + 1
        self.attendees.append(attendee_name)
        self.save()
