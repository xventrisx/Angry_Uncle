__all__=['Task', 'StatusTask']
from django.db import models
from django.contrib.auth.models import User
from .project import *
from .userstory import *

class Task(models.Model):
    name = models.CharField(max_length=250)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_task')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    status = models.ForeignKey('StatusTask', on_delete=models.CASCADE)
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    description = models.TextField()
    time_completion = models.DateField(null=True)
    number = models.IntegerField()

    def __str__(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}'.format(
            self.name,
            self.created_by,
            self.responsible,
            self.status,
            self.user_story,
            self.description,
            self.time_completion,
            self.number,
        )
    



class StatusTask(models.Model):
    alies = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{}, {}'.format(
            self.alies,
            self.name,
        )