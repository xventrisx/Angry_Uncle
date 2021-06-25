from django.db import models
from authentication.models.user import User
from .message import *


class Mentioning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}, {}".format(self.user, self.message, self.date_created)
