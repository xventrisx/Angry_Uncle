from django.db import models
from authentication.models.user import User
from .chat import *


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text_message = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.sender, self.chat, self.text_message, self.date_created)


class WhoRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}, {}".format(self.user, self.date_created, self.message)