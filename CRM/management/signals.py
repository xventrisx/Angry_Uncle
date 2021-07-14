from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from tasker.models.sprint import *
from django.core.mail import send_mail
from .views import change_status_signal, change_responsible_signal
from tasker.models.sprint import *
from tasker.models.issue import *
from tasker.models.userstory import *
from tasker.models.task import *
from API.views import change_status_signal, change_responsible_signal





@receiver(change_status_signal)# сигнал про изминениее статутса спринта
def handler_change_status_signal(sender, **kwargs):
    if isinstance(sender, Sprint):
        send_mail('Изминение статуса Спринта',
                  'Сатус Спринта был изминен',
                  'xventrisx@ukr.net',
                  [sender.responsible.email, sender.created_by.email])
    elif isinstance(sender, Issue):
        send_mail('Изминение статуса Запроса',
                  'Сатус запроса был изминен',
                  'xventrisx@ukr.net',
                  [sender.responsible.email, sender.created_by.email])
    elif isinstance(sender, UserStory):
        responsibles_email = []
        responsibles_email.append(sender.created_by.email)
        for i in sender.responsibles.all():
            responsibles_email.append(i.email)
        send_mail('Изминение статуса Пользовательской истории',
                  'Сатус Пользовательской истории был изминен',
                  'xventrisx@ukr.net',
                  responsibles_email)
    elif isinstance(sender, Task):
        send_mail('Изминение статуса задачи',
                  'Сатус задачи был изминен',
                  'xventrisx@ukr.net',
                  [sender.created_by.email, sender.responsible.email])




@receiver(change_responsible_signal)# сигнал про изминениее статутса спринта
def handler_change_responsible_signal(sender, **kwargs):
    if isinstance(sender, Sprint):
        send_mail('Изминение ответственный Спринта',
        'Ответственный Спринта был изминен',
        'xventrisx@ukr.net',
        [sender.responsible.email])
    elif isinstance(sender, Issue):
        send_mail('Изминение ответственного Запроса',
                  'Ответственный запроса был изминен',
                  'xventrisx@ukr.net',
                  [sender.responsible.email, sender.created_by.email])
    elif isinstance(sender, UserStory):
        responsibles_email = []
        responsibles_email.append(sender.created_by.email)
        for i in sender.responsibles.all():
            responsibles_email.append(i.email)
        send_mail('Изминение ответственного Пользовательской истории',
                  'Ответственный Пользовательской истории был изминен',
                  'xventrisx@ukr.net',
                  responsibles_email)
    elif isinstance(sender, Task):
        send_mail('Изминение ответственного задачи',
                  'Ответственный задачи был изминен',
                  'xventrisx@ukr.net',
                  [sender.created_by.email, sender.responsible.email])