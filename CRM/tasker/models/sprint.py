__all__=['Sprint', 'SprintStatus']
from django.db import models
from django.contrib.auth.models import User
from .project import *

class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sprint')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible_sprint')
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.ForeignKey('SprintStatus', on_delete=models.CASCADE)
    date_create = models.DateField(auto_now_add=True)
    data_update = models.DateField(auto_now=True)
    data_closed = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    number = models.IntegerField()

    def __str__(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(
            self.project,
            self.created_by,
            self.responsible,
            self.name,
            self.description,
            self.status,
            self.date_create,
            self.data_update,
            self.data_closed,
            self.is_active,
            self.number,
        )


class SprintStatus(models.Model):
    alies = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{}, {}'.format(
            self.alies,
            self.name
        )