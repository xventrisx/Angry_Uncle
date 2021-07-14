from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.datastructures import MultiValueDictKeyError
import uuid
from .models.tokenemail import *
from .services import *
from .utilities import *
from django.dispatch import Signal
from tasker.models.project import *
from tasker.models.sprint import *
from tasker.models.issue import *
from tasker.models.userstory import *
from tasker.models.task import *
from tasker.models.coment import *
from django.contrib.auth.models import User

change_status_signal = Signal()
change_responsible_signal = Signal()


@is_auth
def coment_for_task(request, id):
    comentservis = ComentServis(request,id)
    data = comentservis.get_coment_for_task()
    context = {
        'data': data,
    }
    return render(request, 'comentfortask.html', context)


@is_auth
def create_coment_for_sprint(request):
    if request.user.has_perm('tasker.can_add_coment_for_sprint'):
        comentservis = ComentServis(request, id)
        data = comentservis.set_coment_for_sprint()
        return redirect('/management/sprint/{}'.format(data.sprint.id))
    else:
        return HttpResponse('Permission denied', status=403)


@is_auth
def create_coment_for_userstory(request):
    if request.user.has_perm('tasker.can_add_coment_for_userstory'):
        comentservis = ComentServis(request, id)
        data = comentservis.set_coment_for_userstory()
        return redirect('/management/userstory/{}'.format(data.userstories.id))
    else:
        return HttpResponse('Permission denied', status=403)


@is_auth
def create_coment_for_task(request):
    if request.user.has_perm('tasker.can_add_coment_for_task'):
        comentservis = ComentServis(request, id)
        data = comentservis.set_coment_for_task()
        return redirect('/management/task/{}'.format(data.task.id))
    else:
        return render(request, 'NotPermissionCreateComent.html')


@is_auth
def create_coment_for_issue(request):
    comentservis = ComentServis(request, request.POST['issue_id'])
    data = comentservis.set_coment_fot_issue()
    return redirect('/management/issue-info/{}'.format(data.issue.id))


@is_auth
@add_userstory_perm
def create_userstory_for_sprint(request):
    data = add_userstory_for_sprint(request.user, request.POST)
    if data == None:
        return render(request, 'NotCreate.html')
    elif data:
        return redirect('/management/sprint/{}'.format(data.sprint.id))



@is_auth
@change_userstory_perm
def user_story(request, id):
    comentservis = ComentServis(request, id)
    userstory = get_userstory(id=id)
    tasks = get_list_task(id=userstory['userstory'].id)
    coments = comentservis.get_coments_for_userstory()
    form_add_coment = CreateComentForm()
    form_add_task = CreateTaskForm()
    form_starus_userstoty = UserStoryStatusForm()
    form_responsible_form = ResponsibleUserstory()
    context = {
        'userstory': userstory,
        'tasks': tasks,
        'coments': coments,
        'form_add_coment': form_add_coment,
        'form_add_task': form_add_task,
        'form_starus_userstoty': form_starus_userstoty,
        'form_responsible_form': form_responsible_form,
    }
    return render(request, 'userstory.html', context)

@is_auth
@change_userstory_perm
def change_status_userstory(request):
    userstory = get_userstory(request.POST['userstory_id'])
    userstory_status = UserStoryStatusForm(request.POST, instance=userstory['userstory'])
    if userstory_status.is_valid():
        userstory_status.save()
        change_status_signal.send(sender=userstory['userstory'])
        return redirect('/management/userstory/{}'.format(userstory['userstory'].id))


@is_auth
@change_userstory_perm
def change_responsible_userstory(request):
    userstory = get_userstory(request.POST['userstory_id'])
    userstory_responsibls = ResponsibleUserstory(request.POST, instance=userstory['userstory'])
    if userstory_responsibls.is_valid():
        userstory_responsibls.save()
        change_responsible_signal.send(sender=userstory['userstory'])
        return redirect('/management/userstory/{}'.format(userstory['userstory'].id))



@is_auth
@create_task_perm
def create_task_for_userstory(request):
    data = add_task_for_userstory(request.user, request.POST)
    return redirect('/management/userstory/{}'.format(data.user_story.id))


@is_auth
@add_project_perm
def create_project(request):
    data = request.POST
    data = add_project(data)
    return redirect('/management/homepage')


@is_auth
def task(request, id):
    comentservis = ComentServis(request, id)
    task = get_task(id=id)
    coments = comentservis.get_coment_for_task()
    task_status = StatusTaskForm(request.POST, instance=task['task'])
    form_add_coment = CreateComentForm()
    form_responsible = ResponsibleTaskForm()
    context = {
        'task': task,
        'coments': coments,
        'form_add_coment': form_add_coment,
        'task_status': task_status,
        'form_responsible': form_responsible,
    }
    return render(request, 'task.html', context)



@is_auth
@change_task_perm
def change_status_task(request):
    task = get_task(id=request.POST['task_id'])
    task_status = StatusTaskForm(request.POST, instance=task['task'])
    if task_status.is_valid():
        task_status.save()
        change_status_signal.send(sender=task['task'])
        return redirect('/management/task/{}'.format(request.POST['task_id']))


@is_auth
@change_task_perm
def change_responsible_task(request):
    task = get_task(id=request.POST['task_id'])
    task_responsibles = ResponsibleTaskForm(request.POST, instance=task['task'])
    if task_responsibles.is_valid():
        task_responsibles.save()
        change_responsible_signal.send(sender=task['task'])
        return redirect('/management/task/{}'.format(request.POST['task_id']))


@is_auth
def user_info(request, id):
    data = user_inform(id=id)
    context ={
        'data': data,
    }
    return render(request, 'userinfo.html', context)


@is_auth
def my_project(request, id):
    data = project_information(id=id)
    sprint_create_form = CreateSprintForm()
    issue_create_form = CreateIssueForm()
    context = {
        'data': data,
        'sprint_create_form': sprint_create_form,
        'issue_create_form': issue_create_form,
    }
    return render(request, 'project.html', context)


@is_auth
def sprint(request, id):
    comentservis = ComentServis(request, id)
    sprint = get_sprint(id=id)
    userstorys = get_list_userstorys(id=id)
    coments = comentservis.get_coment_for_sprint()
    sprint_status = StatusSprintForm(request.POST, instance=sprint['sprint'])
    responsible_sprint = ChangeResponsibleForm(request.POST, instance=sprint['sprint'])
    form_add_coment = CreateComentForm()
    form_add_userstory = CreateUserStoryForm()
    context = {
        'sprint': sprint,
        'sprint_status': sprint_status,
        'responsible_sprint': responsible_sprint,
        'userstorys': userstorys,
        'coments': coments,
        'form_add_coment': form_add_coment,
        'form_add_userstory': form_add_userstory,
    }
    return render(request, 'sprint.html', context)


@is_auth
@change_sprit_perm
def change_status_sprint(request):
    sprint = get_sprint(id=request.POST['sprint_id'])
    sprint_status = StatusSprintForm(request.POST, instance=sprint['sprint'])
    if sprint_status.is_valid():
        sprint_status.save()
        change_status_signal.send(sender=sprint['sprint'])
        return redirect('/management/sprint/{}'.format(request.POST['sprint_id']))


@is_auth
@change_sprit_perm
def change_responsible_sprint(request):
    sprint = get_sprint(id=request.POST['sprint_id'])
    sprint_status = ChangeResponsibleForm(request.POST, instance=sprint['sprint'])
    if sprint_status.is_valid():
        sprint_status.save()
        change_responsible_signal.send(sender=sprint['sprint'])
        return redirect('/management/sprint/{}'.format(request.POST['sprint_id']))


@is_auth
@add_sprint_perm
def create_sprint(request):
    data = add_sprint(request.user, request.POST)
    context = {
        'data': data,
    }
    if data:
        return render(request, 'SuccessfullyCreatedSprint.html')


@is_auth
@add_issue_perm
def create_issue(request):
    data = add_issue(request.user, request.POST)
    return render(request, 'SuccessfullyCreatedIssue.html')


@is_auth
def list_issues(request, id):
    data = issues_for_project(id)
    context = {
        'data': data,
    }
    return render(request, 'listissues.html', context)


@is_auth
def list_issues_two(request, id):
    data = two_list_issues(request, id)
    context = {
        'data': data,
    }
    return render(request, 'AlternativeTemplate.html', context)


@is_auth
@chenge_issue_perm
def change_status_issue_two(request):
    issue = get_issue(request, request.POST['issue_id'])
    issue_status = StatusIssueForm(request.POST, instance=issue['issue'])
    if issue_status.is_valid():
        issue_status.save()
    return redirect('/management/list-issues-two/{}'.format(request.POST['project_id']))


@is_auth
def issue_info(request, id):
    data = get_issue(request, id)
    comentservis = ComentServis(request, data['issue'].id)
    coments = comentservis.get_coments_for_issue()
    context = {
        'data': data,
        'coments': coments,
    }
    return render(request, 'IssueInfo.html', context)

@is_auth
@chenge_issue_perm
def change_status_issue(request):
    issue = get_issue(request, request.POST['issue_id'])
    issue_status = StatusIssueForm(request.POST, instance=issue['issue'])
    if issue_status.is_valid():
        issue_status.save()
        change_status_signal.send(sender=issue['issue'])
    return redirect('/management/issue-info/{}'.format(request.POST['issue_id']))


@is_auth
@chenge_issue_perm
def change_responsible_issue(request):
    data = get_issue(request, request.POST['issue_id'])
    if data['responsible_form'].is_valid():
        data['responsible_form'].save()
        return redirect('/management/issue-info/{}'.format(request.POST['issue_id']))


@is_auth
def members_project(request, id):
    data = members_in_project(id)
    context = {'data': data}
    return render(request, 'membersinproject.html', context)


@is_auth
def home_page(request):# вид главной страницы. можна создать проект, пригласить пользователя в проект.
    my_projects = request.user.projects.all()
    my_create = request.user.manage_projects.all()
    form_add_project = CreateProjectForm()
    context = {
        'my_projects': my_projects,
        'form_add_project': form_add_project,
    }
    return render(request, 'homepage.html', context)


def enter(request):# вид страницы входа
    loginform = LoginForm()
    context = {'loginform': loginform}
    return render(request, 'login.html', context)


def emailconfirmation(request):# переход по токену после подтверждения електронной почты
    try:
        tokenuser = TokenEmail.objects.get(token=request.GET['key'])
    except ObjectDoesNotExist:
        return render(request,'notinvitation.html')
    else:
        if tokenuser:
            project_id = tokenuser.project.id
            chekin = CheckinForm()
            context = {
                'chekin': chekin,
                'project_id': project_id
            }
            TokenEmail.objects.get(token=request.GET['key']).delete()
            return render(request, 'chekin.html', context)

@is_auth
@send_invition_perm
def send_invitation(request):# страница отповищения успешной отправки о пиглашение.
    data = dict(request.POST)
    data['web']=True
    send_invit(data=data)
    return render(request, 'shippingconfirmation.html')


@is_auth
@send_invition_perm
def invite(request):# вид страниц отправки приглашения
    tokenemail = InvitaForm()
    context = {'tokenemail': tokenemail}
    return render(request, 'sendnvitation.html', context)


def entrance(request):# авторизация пользователя
    user = authenticate( 
        username=request.POST["username"],
        password=request.POST["password"],
    )
    if user is not None:
        login(request, user)
        return redirect('/management/homepage')
    else:
        return render(request, 'userisnotfound.html')


def log_out(request):# выход с авторизации
    logout(request) #
    return redirect('/management/login')


def register(request):# функция регистрации пользователя
    if create_user(data=request.POST) != None:
        return render(request, 'sentnotification.html')
    else:
         return render(request, 'emailisused.html')


@is_auth
@add_sprint_perm
def form_add_sprint(request, id):
    sprint_create_form = CreateSprintForm()
    project_id = id
    context = {
        'project_id': project_id,
        'sprint_create_form': sprint_create_form,
    }
    return render(request, 'AddSprint.html', context)


@is_auth
@add_issue_perm
def form_add_issue(request, id):
    issue_create_form = CreateIssueForm()
    project_id = id
    context = {
        'project_id': project_id,
        'issue_create_form': issue_create_form,
    }
    return render(request, 'AddIssue.html', context)



@is_auth
def search_box(request):
    data = search(request)
    context = {
        'data': data,
    }
    if data:
        return render(request, 'FoundObjects.html', context)
    else:
        return render(request, 'notfoundnumber.html')

