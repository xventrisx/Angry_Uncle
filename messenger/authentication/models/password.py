from django.db import models



class Ticket(models.Model):
    password = models.TextField()
    number_phone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.number_phone)