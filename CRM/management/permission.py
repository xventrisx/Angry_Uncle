__all__=[
    'Adminproject',
    'Managerprojects',
    'Performer',
]
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models.tokenemail import *
from tasker.models.project import *
from tasker.models.sprint import *
from tasker.models.issue import *
from tasker.models.userstory import *
from tasker.models.task import *
from tasker.models.coment import *



class Adminproject:
    def __init__(self):
        self.list_perm_name = [
            'add_coment',
            'change_coment',
            'view_coment',
            'add_issue',
            'change_issue',
            'view_issue',
            'add_issuestatus',
            'change_issuestatus',
            'view_issuestatus',
            'add_project',
            'change_project',
            'view_project',
            'add_sprint',
            'can_add_coment_for_sprint',
            'change_sprint',
            'view_sprint',
            'add_sprintstatus',
            'change_sprintstatus',
            'view_sprintstatus',
            'add_statustask',
            'change_statustask',
            'view_statustask',
            'add_task',
            'can_add_coment_for_task',
            'change_task',
            'view_task',
            'add_userstory',
            'can_add_coment_for_userstory',
            'change_userstory',
            'view_userstory',
            'add_userstorystatus',
            'change_userstorystatus',
            'view_userstorystatus',
            'can_add_coment_for_issue',
            'send_invitation',
        ]
        self.perm_group = Group()


    def set_name_group(self, name):
        self.perm_group.name = name
        self.perm_group.save()


    def add_perm_for_group(self):
        try:
            for x in self.list_perm_name:
                perm = Permission.objects.get(codename=x)
                self.perm_group.permissions.add(perm)
        except ObjectDoesNotExist:
            list_word = x.split('_')
            if list_word[-1] == 'sprint':
                content_type = ContentType.objects.get_for_model(Sprint)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for sprint',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)
            elif list_word[-1] == 'task':
                content_type = ContentType.objects.get_for_model(Task)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for task',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)
            elif list_word[-1] == 'userstory':
                content_type = ContentType.objects.get_for_model(UserStory)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for userstory',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)
            elif list_word[-1] == 'issue':
                content_type = ContentType.objects.get_for_model(Issue)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for issue',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)
            elif list_word[-1] == 'invitation':
                content_type = ContentType.objects.get_for_model(TokenEmail)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can send invitation',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)



class Managerprojects:
    def __init__(self):
        self.list_perm_name = [
            'add_coment',
            'view_coment',
            'add_issue',
            'change_issue',
            'view_issue',
            'add_issuestatus',
            'change_issuestatus',
            'view_issuestatus',
            'view_project',
            'add_sprint',
            'can_add_coment_for_sprint',
            'change_sprint',
            'view_sprint',
            'add_sprintstatus',
            'change_sprintstatus',
            'view_sprintstatus',
            'add_statustask',
            'change_statustask',
            'view_statustask',
            'add_task',
            'can_add_coment_for_task',
            'change_task',
            'view_task',
            'add_userstory',
            'can_add_coment_for_userstory',
            'change_userstory',
            'view_userstory',
            'add_userstorystatus',
            'change_userstorystatus',
            'view_userstorystatus',
            'can_add_coment_for_issue',
        ]
        self.perm_group = Group()


    def set_name_group(self, name):
        self.perm_group.name = name
        self.perm_group.save()


    def add_perm_for_group(self):
        try:
            for x in self.list_perm_name:
                perm = Permission.objects.get(codename=x)
                self.perm_group.permissions.add(perm)
        except ObjectDoesNotExist:
            list_word = x.split('_')
            if list_word[-1] == 'sprint':
                content_type = ContentType.objects.get_for_model(Sprint)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for sprint',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)
            elif list_word[-1] == 'task':
                content_type = ContentType.objects.get_for_model(Task)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for task',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)
            elif list_word[-1] == 'userstory':
                content_type = ContentType.objects.get_for_model(UserStory)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for userstory',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)
            elif list_word[-1] == 'issue':
                content_type = ContentType.objects.get_for_model(Issue)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for issue',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)



class Performer:
    def __init__(self):
        self.list_perm_name = [
            'add_coment',
            'view_coment',
            'view_issue',
            'change_issuestatus',
            'view_issuestatus',
            'view_project',
            'can_add_coment_for_sprint',
            'change_sprint',
            'view_sprint',
            'change_sprintstatus',
            'view_sprintstatus',
            'change_statustask',
            'view_statustask',
            'can_add_coment_for_task',
            'view_task',
            'can_add_coment_for_userstory',
            'view_userstory',
            'change_userstorystatus',
            'view_userstorystatus',
            'can_add_coment_for_issue',
        ]
        self.perm_group = Group()


    def set_name_group(self, name):
        self.perm_group.name = name
        self.perm_group.save()


    def add_perm_for_group(self):
        try:
            for x in self.list_perm_name:
                perm = Permission.objects.get(codename=x)
                self.perm_group.permissions.add(perm)
        except ObjectDoesNotExist:
            list_word = x.split('_')
            if list_word[-1] == 'sprint':
                content_type = ContentType.objects.get_for_model(Sprint)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for sprint',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)
            elif list_word[-1] == 'task':
                content_type = ContentType.objects.get_for_model(Task)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for task',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)
            elif list_word[-1] == 'userstory':
                content_type = ContentType.objects.get_for_model(UserStory)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for userstory',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)
            elif list_word[-1] == 'issue':
                content_type = ContentType.objects.get_for_model(Issue)
                permission = Permission.objects.create(
                    codename=x,
                    name='Can add coment for issue',
                    content_type=content_type
                )
                self.perm_group.permissions.add(permission)