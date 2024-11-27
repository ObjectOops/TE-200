from hashlib import sha256

from django.db import models

from util import stringify_attrs

class User(models.Model):
    username = models.CharField(max_length=64)
    hash_sha256 = models.CharField(max_length=256)
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return stringify_attrs(
            self.username, self.hash_sha256, "Instructor" if self.is_instructor else "Student"
        )
    
    def authenticate(self, password):
        hash_unauthenticated = sha256(password.encode("utf-8")).hexdigest()
        return hash_unauthenticated == self.hash_sha256
