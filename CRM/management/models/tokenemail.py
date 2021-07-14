__all__=['TokenEmail']
from django.db import models
from django.contrib.auth.models import User
from tasker.models.project import *


class TokenEmail(models.Model):
    email = models.CharField(max_length=50)
    token = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return "{}, {}, {}".format(
            self.email,
            self.token,
            self.project,
        )