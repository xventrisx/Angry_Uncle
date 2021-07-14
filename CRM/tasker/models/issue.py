__all__=['Issue', 'IssueStatus']
from django.db import models
from django.contrib.auth.models import User
from .project import * 

class Issue(models.Model):
    name = models.CharField(max_length=250)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_issues')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues', null=True, blank=True)
    status = models.ForeignKey('IssueStatus', on_delete=models.CASCADE)
    body = models.TextField()
    date_create = models.DateField(auto_now_add=True)
    data_update = models.DateField(auto_now=True)
    data_closed = models.DateField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}, {}'.format(
            self.created_by,
            self.responsible,
            self.status,
            self.body,
            self.date_create,
            self.data_update,
            self.data_closed,
            self.project,
            self.number,
        )
    

class IssueStatus(models.Model):
    alies = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{}, {}'.format(
            self.alies,
            self.name,
        )
