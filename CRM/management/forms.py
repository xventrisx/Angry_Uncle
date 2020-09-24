__all__=[
    'LoginForm',
    'CheckinForm',
    'InvitaForm',
    'CreateProjectForm',
    'CreateSprintForm',
    'CreateIssueForm',
    'CreateComentForm',
    'CreateUserStoryForm',
    'CreateTaskForm',
    'StatusSprintForm',
    'StatusIssueForm',
    'StatusTaskForm',
    'ChangeResponsibleForm',
    'UserStoryStatusForm',
    'ResponsibleTaskForm',
    'ResponsibleUserstory',
]


from django.forms import ModelForm
from .models.tokenemail import *
from django.contrib.auth.models import User
from tasker.models.project import *
from tasker.models.sprint import *
from tasker.models.issue import *
from tasker.models.userstory import *
from tasker.models.task import *
from tasker.models.coment import *


class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'admin',
            'name',
            'description',
            'members',
        ]


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = [
        'username',
        'password',
        ]


class CheckinForm(ModelForm):
    class Meta:
        model = User
        fields = [
        'username',
        'password',
        'email',
        'first_name',
        'last_name',
        ]


class InvitaForm(ModelForm):
    class Meta:
        model = TokenEmail
        fields = [
            'email',
            'project',
        ]


class CreateSprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = [
            'responsible',
            'name',
            'description',
            'status',
        ]


class CreateIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = [
            'name',
            'responsible',
            'status',
            'body',
            'project',
        ]


class CreateComentForm(ModelForm):
    class Meta:
        model = Coment
        fields = [
            'body',
        ]


class CreateUserStoryForm(ModelForm):
    class Meta:
        model = UserStory
        fields = [
            'name',
            'responsibles',
            'status',
            'description',
        ]


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'responsible',
            'status',
            'description',
            'time_completion',
        ]


class StatusSprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = [
            'status',
        ]


class UserStoryStatusForm(ModelForm):
    class Meta:
        model = UserStory
        fields = [
            'status',
        ]


class StatusIssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = [
            'status',
        ]


class StatusTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'status',
        ]


class ResponsibleTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'responsible'
        ]


class ChangeResponsibleForm(ModelForm):
    class Meta:
        model = Issue
        fields = [
            'responsible',
        ]


class ResponsibleUserstory(ModelForm):
    class Meta:
        model = UserStory
        fields = [
            'responsibles',
        ]