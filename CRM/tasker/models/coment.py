__all__=['Coment']
from django.db import models
from django.contrib.auth.models import User
from .userstory import *
from .sprint import *
from .task import *
from .issue import *


class Coment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coments', blank=True, null=True)
    userstories = models.ForeignKey(UserStory, on_delete=models.CASCADE, related_name='coments', blank=True, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, related_name='coments', blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='coments', blank=True, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='coments', blank=True, null=True)
    body = models.TextField()
    date_create = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}".format(
            self.created_by,
            self.userstories,
            self.sprint,
            self.task,
            self.issue,
            self.body,
            self.date_create,
        )