from django.db import models
from django.db.models import F

from util import stringify_attrs

class Class(models.Model):
    name = models.CharField(max_length=64)
    signin_required = models.BooleanField(default=False)
    route_id = models.CharField(max_length=6)
    in_session = models.BooleanField(default=True)
    students = models.JSONField(default=list)
    student_count = models.IntegerField(default=0)

    def __str__(self):
        return stringify_attrs(
            self.name, self.signin_required, self.route_id, self.student_count, self.in_session
        )

    def mark_student(self, username):
        self.student_count = F("student_count") + 1
        self.students.append(username)
