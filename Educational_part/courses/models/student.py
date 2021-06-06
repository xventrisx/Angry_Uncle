from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return '{0}, {1}, {2}'.format(
            self.first_name,
            self.last_name,
            self.email,
        )
