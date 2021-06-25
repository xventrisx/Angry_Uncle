from django.db import models
from authentication.models.user import User


class Contact(models.Model):
    whose = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contacts')
    members = models.ManyToManyField(User, related_name='in_contacts')

    def __str__(self):
        return "{}, {}".format(self.whose, self.members)
