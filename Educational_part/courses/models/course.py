from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(
            self.name,
            self.description,
            self.start_date,
            self.end_date
        )
