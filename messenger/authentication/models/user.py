from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.IntegerField(null=True, blank=True, unique=True)
    last_activity = models.DateTimeField(null=True)

    def __str__(self):
        return '{}'.format(self.username)
