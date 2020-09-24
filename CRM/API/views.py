from management.models.tokenemail import *
from management.services import *
from management.utilities import *
from .serializers import *
from django.contrib.auth.models import User
from tasker.models.task import *
from tasker.models.issue import *
from tasker.models.sprint import *
from tasker.models.userstory import *
from rest_framework import generics
from rest_framework import response as rest_response
from rest_framework import status as rest_status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.dispatch import Signal


change_status_signal = Signal()
change_responsible_signal = Signal()



class InviteCreateAPIview(generics.CreateAPIView):
    serializer_class = InvitSendSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['web'] = False
        key = send_anvite_api(data=data)
        keys = dict(token = key)
        return rest_response.Response(data={'detail': keys}, status=rest_status.HTTP_200_OK)


class InvitTakesAPIview(generics.CreateAPIView):
    serializer_class = InvitTakesSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        tokenmail = TokenEmail.objects.filter(token=data['token']).exists()
        if tokenmail:
            user = create_user(data=data)
            if user != None:
                user = dict(user_id = user.id)
                return rest_response.Response(data={'detail': user}, status=rest_status.HTTP_200_OK)
            else:
                return rest_response.Response(data={'detail': user}, status=rest_status.HTTP_200_OK)
        else:
            return rest_response.Response(data={'detail': user}, status=rest_status.HTTP_200_OK)

class IssueSendAPIview(generics.CreateAPIView):
    serializer_class = IssueCreateSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data = add_issue(request.user, data)
        return rest_response.Response(data={'detail':''}, status=rest_status.HTTP_200_OK)


class IssuesListAPIview(generics.ListAPIView):
    serializer_class = IssueReturnSerializer

    def list(self, request, id):
        data = issues_for_project(id=id)
        serializer = self.serializer_class(data['issues'], many=True)
        return rest_response.Response(data=serializer.data, status=rest_status.HTTP_200_OK)


class UserCreateAPIview(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"]
        )
        user.save()
        return rest_response.Response(data={'detail': ''}, status=rest_status.HTTP_200_OK)



class ProjectAddAPIview(generics.CreateAPIView):
    serializer_class = ProjectAddSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        project_resalt = add_project_api(data)
        return rest_response.Response(data={'detail': ''}, status=rest_status.HTTP_200_OK)


class ProjectsAdminListAPIview(generics.ListAPIView):
    serializer_class = ProjectAddSerializer

    def get_queryset(self):
        return self.request.user.manage_projects.all()


class ProjectsListAPIview(generics.ListAPIView):
    serializer_class = ProjectAddSerializer

    def get_queryset(self):
        return self.request.user.projects.all()



class ProjectListAPIview(generics.RetrieveAPIView):
    serializer_class = ProjectAddSerializer

    def get_queryset(self):
        return self.request.user.projects.all()



class SprintAddAPIview(generics.CreateAPIView):
    serializer_class = SprintAddSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        sprint = add_sprint(request.user, data)
        return rest_response.Response(data={'detail': ''}, status=rest_status.HTTP_200_OK)


class SprintsListfoProjectAPIview(generics.ListAPIView):
    serializer_class = SprintReturnSerializer

    def list(self, request, id):
        data = project_information(id=id)
        serializer = self.serializer_class(data['sprint'], many=True)
        return rest_response.Response(data=serializer.data, status=rest_status.HTTP_200_OK)


class UserstoryAddAPIview(generics.CreateAPIView):
    serializer_class = UserStoryAddSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        userstory = add_userstory_for_sprint(request.user, data)
        return rest_response.Response(data={'detail': ''}, status=rest_status.HTTP_200_OK)


class UserstorysListSprintAPIview(generics.ListAPIView):
    serializer_class = UserStoryReturnSerializer

    def list(self, request, id):
        data = get_list_userstorys(id=id)
        serializer = self.serializer_class(data['list_userstorys'], many=True)
        return rest_response.Response(data=serializer.data, status=rest_status.HTTP_200_OK)


class TaskAddAPIview(generics.CreateAPIView):
    serializer_class = TaskAddSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = add_task_for_userstory(request.user, data)
        return rest_response.Response(data={'detail': ''}, status=rest_status.HTTP_200_OK)


class TaskListUserStoryAPIview(generics.ListAPIView):
    serializer_class = TaskReturnSerializer

    def list(self, request, id):
        data = get_list_task(id=id)
        serializer = self.serializer_class(data['tasks'], many=True)
        return rest_response.Response(data=serializer.data, status=rest_status.HTTP_200_OK)


class TaskReturnAPIview(generics.RetrieveAPIView):
    serializer_class = TaskReturnSerializer


    def get_queryset(self):
        return Task.objects.all()


class ComentAddSprintAPIview(generics.CreateAPIView):
    serializer_class = ComentAddforSprintSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        servis_coment = ComentServisAPI(request.user, data)
        coment = servis_coment.set_coment_for_spint_api()
        return rest_response.Response(data={'detail': ''}, status=rest_status.HTTP_200_OK)


class ComentAddUserstoryAPIview(generics.CreateAPIView):
    serializer_class = ComentAddforUserstorySerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        servis_coment = ComentServisAPI(request.user, data)
        coment = servis_coment.set_coment_for_userstory_api()
        return rest_response.Response(data={'detail': ''}, status=rest_status.HTTP_200_OK)


class ComentAddTaskAPIview(generics.CreateAPIView):
    serializer_class = ComentAddforTaskSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        servis_coment = ComentServisAPI(request.user, data)
        coment = servis_coment.set_coment_for_task_api()
        return rest_response.Response(data={'detail': ''}, status=rest_status.HTTP_200_OK)


class IssueChangeResponsibleAPIview(generics.UpdateAPIView):
    serializer_class = IssueResponsibleUpdateSerializer

    def get_queryset(self):
        issue = get_issue(self.request, id=self.kwargs['pk'])
        change_responsible_signal.send(sender=issue['issue'])
        return Issue.objects.all()


class IssueChangeStatusAPIview(generics.UpdateAPIView):
    serializer_class = IssueStatusUpdateSerializer

    def get_queryset(self):
        issue = get_issue(self.request, id=self.kwargs['pk'])
        change_status_signal.send(sender=issue['issue'])
        return Issue.objects.all()


class IssueUpdateAPIview(generics.UpdateAPIView):
    serializer_class = IssueUpdateSerializer

    def get_queryset(self):
        return Issue.objects.all()


class SprintChandeResponsibleAPIview(generics.UpdateAPIView):
    serializer_class = SprintResponsibleUpdateSerializer

    def get_queryset(self):
        sprint = get_sprint(id=self.kwargs['pk'])
        change_responsible_signal.send(sender=sprint['sprint'])
        return Sprint.objects.all()


class SprintChangeStatusAPIview(generics.UpdateAPIView):
    serializer_class = SprintStatusUpdateSerializer

    def get_queryset(self):
        sprint = get_sprint(id=self.kwargs['pk'])
        change_status_signal.send(sender=sprint['sprint'])
        return Sprint.objects.all()


class SprintUpdateAPIview(generics.UpdateAPIView):
    serializer_class = SprintUpdateSerializer

    def get_queryset(self):
        return Sprint.objects.all()


class UserStoryChangeResponsibleAPIview(generics.UpdateAPIView):
    serializer_class = UserStoryUpdateResponsiblesSerializer

    def get_queryset(self):
        userstory = get_userstory(id=self.kwargs['pk'])
        change_responsible_signal.send(sender=userstory['userstory'])
        return UserStory.objects.all()


class UserStoryChangeStatusAPIview(generics.UpdateAPIView):
    serializer_class = UserStoryStatusUpdateSerializer

    def get_queryset(self):
        userstory = get_userstory(id=self.kwargs['pk'])
        change_status_signal.send(sender=userstory['userstory'])
        return UserStory.objects.all()


class TaskChangeResponsibleAPIview(generics.UpdateAPIView):
    serializer_class = TaskUpdateResponsibleSerializer

    def get_queryset(self):
        task = get_task(id=self.kwargs['pk'])
        change_responsible_signal.send(sender=task['task'])
        return Task.objects.all()


class TaskChangeStatusAPIview(generics.UpdateAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = TaskUpdateStatusSerializer

    def get_queryset(self):
        task = get_task(id=self.kwargs['pk'])
        change_status_signal.send(sender=task['task'])
        return Task.objects.all()


    @change_task_perm
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)