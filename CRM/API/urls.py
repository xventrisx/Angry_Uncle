from django.urls import path
from API.views import *
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('send-invit-api', InviteCreateAPIview.as_view()),
    path('takes-invit-serializer', InvitTakesAPIview.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view()),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('issue-send-api/', IssueSendAPIview.as_view()),
    path('createuser', UserCreateAPIview.as_view()),
    path('project-add-api/', ProjectAddAPIview.as_view()),
    path('sprint-add-api/', SprintAddAPIview.as_view()),
    path('userstory-add-api/', UserstoryAddAPIview.as_view()),
    path('task-add-api/', TaskAddAPIview.as_view()),
    path('add-coment-for-sprint-api/', ComentAddSprintAPIview.as_view()),
    path('add-coment-for-userstory-api/', ComentAddUserstoryAPIview.as_view()),
    path('add-coment-for-task-api/', ComentAddTaskAPIview.as_view()),
    path('get-projects-for-user_admin/', ProjectsAdminListAPIview.as_view()),
    path('get-projects-for-user/', ProjectsListAPIview.as_view()),
    path('get-project-for-user/<int:pk>', ProjectListAPIview.as_view()),
    path('get-sprints-for-projects/<int:id>', SprintsListfoProjectAPIview.as_view()),
    path('get-userstory-for-sprint/<int:id>', UserstorysListSprintAPIview.as_view()),
    path('get-tasks-for-userstory/<int:id>', TaskListUserStoryAPIview.as_view()),
    path('get-issues-for-projects/<int:id>',IssuesListAPIview.as_view()),
    path('get-task-for-userstory/<int:pk>', TaskReturnAPIview.as_view()),
    path('update-issue-api/<int:pk>', IssueUpdateAPIview.as_view()),
    path('update-responsible-issue-api/<int:pk>', IssueChangeResponsibleAPIview.as_view()),
    path('update-status-issue-api/<int:pk>', IssueChangeStatusAPIview.as_view()),
    path('update-responsible-sprint-api/<int:pk>', SprintChandeResponsibleAPIview.as_view()),
    path('update-status-sprint-api/<int:pk>', SprintChangeStatusAPIview.as_view()),
    path('update-sprint-api/<int:pk>', SprintUpdateAPIview.as_view()),
    path('update-userstory-responsible-api/<int:pk>', UserStoryChangeResponsibleAPIview.as_view()),
    path('update-userstory-status-api/<int:pk>', UserStoryChangeStatusAPIview.as_view()),
    path('update-task-responsible-api/<int:pk>', TaskChangeResponsibleAPIview.as_view()),
    path('update-task-status-api/<int:pk>', TaskChangeStatusAPIview.as_view()),
]