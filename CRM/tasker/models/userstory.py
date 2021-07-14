__all__=['UserStory', 'UserStoryStatus']
from django.db import models
from django.contrib.auth.models import User
from .project import *
from .sprint import *


class UserStory(models.Model):
    name = models.CharField(max_length=250,)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_userstorys')
    responsibles = models.ManyToManyField(User, related_name='performers_userstorys', blank=True)
    status = models.ForeignKey('UserStoryStatus', on_delete=models.CASCADE)
    description = models.TextField()
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, related_name='userstorys')
    date_create = models.DateField(auto_now_add=True)
    data_update = models.DateField(auto_now=True)
    data_closed = models.DateField(blank=True, null=True)
    number = models.IntegerField()

    def __str__(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(
            self.name,
            self.created_by,
            self.responsibles,
            self.status,
            self.description,
            self.sprint,
            self.date_create,
            self.data_update,
            self.data_closed,
            self.number,
        )
    


class UserStoryStatus(models.Model):
    alies = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{}, {}'.format(
            self.alies,
            self.name,
        )
