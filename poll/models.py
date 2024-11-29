from random import randint
from django.db import models
from django.utils import timezone

from dashboard.models import ClassSession
from util import generate_route_id, sha256_hash, stringify_attrs

class Poll(models.Model):
    name = models.CharField(max_length=64)
    route_id = models.CharField(max_length=6, default=generate_route_id)
    is_open = models.BooleanField(default=True)

    answers = models.JSONField(default=list)
    creation = models.DateTimeField("creation_date", default=timezone.now)
    owner = models.ForeignKey(ClassSession, on_delete=models.CASCADE)

    def __str__(self):
        return stringify_attrs(self.name, self.route_id, self.is_open)
    
    def add_answer(self, username, answer):
        self.answers.append(f"{username}: {answer} @ {timezone.now()}")
