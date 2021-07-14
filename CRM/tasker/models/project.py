__all__=['Project']
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manage_projects', null=True, blank=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='projects',  blank=True)
    date_create = models.DateField(auto_now_add=True)
    data_update = models.DateField(auto_now=True)
    data_closed = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}, {}'.format(
            self.admin,
            self.name,
            self.description,
            self.members,
            self.date_create,
            self.data_update,
            self.data_closed,
            self.is_active,
            self.count,
        )