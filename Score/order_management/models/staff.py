__all__ = [
    'Staff'
]

from django.contrib.auth.models import User
from django.db import models


class Staff(User):
    '''
    Модель персонал описывает имя сотрудника,
    личный номер телефона,
    и дату крайних действий в системе.
    '''

    name = models.CharField(max_length=50)
    phone = models.IntegerField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True)

    def __str__(self):
        return '{0}, {1}, {2}'.format(
            self.name,
            self.phone,
            self.last_activity,
        )
