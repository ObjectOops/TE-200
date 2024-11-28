from random import randint
from django.db import models
from django.db.models import F
from django.utils import timezone

from login.models import User
from util import sha256_hash, stringify_attrs

class ClassSession(models.Model):
    name = models.CharField(max_length=64)
    signin_required = models.BooleanField(default=False)
    route_id = models.CharField(max_length=6)
    in_session = models.BooleanField(default=True)
    students = models.JSONField(default=list)
    student_count = models.IntegerField(default=0)

    creation = models.DateTimeField("creation_date", default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return stringify_attrs(
            self.name, self.route_id, self.signin_required, self.student_count, self.creation
        )

    def mark_student(self, username):
        self.student_count = F("student_count") + 1
        self.students.append(username)
    
    def generate_route_id(self):
        seed = hex(randint(0x0, 0xFFFFFF))[2:]
        self.route_id = sha256_hash(seed)[0:6]
