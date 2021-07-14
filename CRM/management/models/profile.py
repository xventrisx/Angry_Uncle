__all__=['Profile']
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_status = models.BooleanField(default=False)

    def __str__(self):
        return "{}, {}".format(self.user, self.admin_status)