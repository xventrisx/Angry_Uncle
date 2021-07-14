__all__ = [
    'UserCreateSerializer',
    'InvitSendSerializer',
    'InvitTakesSerializer',
    'IssueCreateSerializer',
    'ProjectAddSerializer',
    'ProjectDataSerializer',
    'SprintAddSerializer',
    'UserStoryAddSerializer',
    'TaskAddSerializer',
    'ComentAddforSprintSerializer',
    'ComentAddforUserstorySerializer',
    'ComentAddforTaskSerializer',
    'SprintReturnSerializer',
    'UserDataSerializer',
    'StatusSerializer',
    'UserStoryReturnSerializer',
    'TaskReturnSerializer',
    'IssueReturnSerializer',
    'MembersProjectsSerializer',
    'ComentsReturnSerializer',
    'IssueUpdateSerializer',
    'SprintUpdateSerializer',
    'IssueResponsibleUpdateSerializer',
    'IssueStatusUpdateSerializer',
    'SprintResponsibleUpdateSerializer',
    'SprintStatusUpdateSerializer',
    'UserStoryUpdateResponsiblesSerializer',
    'UserStoryStatusUpdateSerializer',
    'TaskUpdateResponsibleSerializer',
    'TaskUpdateStatusSerializer',
]

from rest_framework import serializers
from django.contrib.auth.models import User
from management.models.tokenemail import *
from tasker.models.issue import *
from tasker.models.project import *
from tasker.models.sprint import *
from tasker.models.userstory import *
from tasker.models.task import *
from tasker.models.coment import *


class ComentsReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coment
        fields = [
            'created_by',
            'body',
            'date_create',
        ]



class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprintStatus
        fields = [
            'alies',
            'name',
        ]



class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =[
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        ]


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =[
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class InvitSendSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField()
    class Meta:
        model = TokenEmail
        fields = [
            'email',
            'project_id',
        ]


class InvitTakesSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    class Meta:
        model = TokenEmail
        fields = [
            'token',
            'username',
            'password',
            'first_name',
            'last_name',
        ]


class IssueCreateSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField()
    class Meta:
        model = Issue
        fields = [
            'name',
            'created_by',
            'responsible',
            'status',
            'body',
            'project_id',
        ]



class ProjectAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'admin',
            'name',
            'description',
            'members',
        ]


class ProjectDataSerializer(serializers.ModelSerializer):
    admin = UserDataSerializer()
    members = UserDataSerializer(many=True)
    class Meta:
        model = Project
        fields = [
            'admin',
            'name',
            'description',
            'members',
            'date_create',
            'data_update',
            'data_closed',
            'is_active',

        ]


class SprintAddSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField()
    class Meta:
        model = Sprint
        fields = [
            'responsible',
            'name',
            'description',
            'status',
            'project_id',
        ]




class SprintReturnSerializer(serializers.ModelSerializer):
    project = ProjectAddSerializer()
    created_by = UserDataSerializer()
    responsible = UserDataSerializer()
    status = StatusSerializer()
    coments = ComentsReturnSerializer(many=True)
    class Meta:
        model = Sprint
        fields = [
            'project',
            'created_by',
            'responsible',
            'name',
            'description',
            'status',
            'date_create',
            'data_update',
            'data_closed',
            'is_active',
            'number',
            'coments'
        ]


class UserStoryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStory
        fields = [
            'name',
            'responsibles',
            'status',
            'description',
            'sprint',
        ]


class UserStoryReturnSerializer(serializers.ModelSerializer):
    created_by = UserDataSerializer()
    responsibles = UserDataSerializer(many=True)
    status = StatusSerializer()
    sprint = SprintAddSerializer()
    coments = ComentsReturnSerializer(many=True)
    class Meta:
        model = UserStory
        fields = [
            'name',
            'created_by',
            'responsibles',
            'status',
            'description',
            'sprint',
            'date_create',
            'data_update',
            'data_closed',
            'number',
            'coments',
        ]


class TaskAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'name',
            'responsible',
            'status',
            'user_story',
            'description',
            'time_completion',
        ]


class TaskReturnSerializer(serializers.ModelSerializer):
    created_by = UserDataSerializer()
    responsible = UserDataSerializer()
    status = StatusSerializer()
    user_story = UserStoryAddSerializer()
    coments = ComentsReturnSerializer(many=True)
    class Meta:
        model = Task
        fields =[
            'name',
            'created_by',
            'responsible',
            'status',
            'user_story',
            'description',
            'time_completion',
            'number',
            'coments',
        ]


class ComentAddforSprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coment
        fields = [
            'sprint',
            'body',
        ]


class ComentAddforUserstorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Coment
        fields = [
            'userstories',
            'body',
        ]


class ComentAddforTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coment
        fields = [
            'task',
            'body',
        ]


class IssueReturnSerializer(serializers.ModelSerializer):
    created_by = UserDataSerializer()
    responsible = UserDataSerializer()
    status = StatusSerializer()
    project = ProjectDataSerializer()
    class Meta:
        model = Issue
        fields = [
            'name',
            'created_by',
            'responsible',
            'status',
            'body',
            'date_create',
            'data_update',
            'data_closed',
            'project',
        ]


class MembersProjectsSerializer(serializers.ModelSerializer):
    members = UserDataSerializer(many=True)
    class Meta:
        model = Project
        fields = [
            'members',
        ]


class IssueResponsibleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'responsible',
        ]


class IssueStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'status',
        ]


class IssueUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'body',
            'data_closed',
        ]


class SprintResponsibleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            'responsible',
        ]


class SprintStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            'status',
        ]


class SprintUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = [
            'description',
            'data_closed',
            'is_active',
        ]


class UserStoryUpdateResponsiblesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStory
        fields = [
            'responsibles',
        ]


class UserStoryStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStory
        fields = [
            'status',
        ]


class TaskUpdateResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'responsible',
        ]

class TaskUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'status',
        ]