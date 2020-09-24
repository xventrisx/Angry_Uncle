__all__=[
    'search',
    'create_user',
    'add_project',
    'send_invit',
    'project_information',
    'get_sprint',
    'members_in_project',
    'issues_for_project',
    'two_list_issues',
    'get_issue',
    'user_inform',
    'get_list_userstorys',
    'get_userstory',
    'get_list_task',
    'get_task',
    'add_sprint',
    'add_issue',
    'add_userstory_for_sprint',
    'add_task_for_userstory',
    'ComentServis',
    'Counter',
    'change_responsible',
    'send_anvite_api',
    'add_project_api',
    'ComentServisAPI',
]


from django.core.mail import send_mail
from .models.tokenemail import *
from django.contrib.auth.models import User
import uuid
from tasker.models.project import *
from tasker.models.sprint import *
from tasker.models.issue import *
from tasker.models.userstory import *
from tasker.models.task import *
from tasker.models.coment import *
from .forms import *
from django.db.models import Q
from django.dispatch import Signal



change_responsible = Signal()


def search(request):
    Q_name = Q(name__contains=request.GET['search'])
    Q_created_1 = Q(created_by__username__contains=request.GET['search'])
    Q_created_2 = Q(created_by__first_name__contains=request.GET['search'])
    Q_created_3 = Q(created_by__last_name__contains=request.GET['search'])
    Q_created_4 = Q(created_by__email__contains=request.GET['search'])
    Q_description = Q(description__contains=request.GET['search'])
    Q_number = Q(number=request.GET['search'])
    Q_body = Q(body__contains=request.GET['search'])
    Q_responsible_1 = Q(responsible__username__contains=request.GET['search'])
    Q_responsible_2 = Q(responsible__first_name__contains=request.GET['search'])
    Q_responsible_3 = Q(responsible__last_name__contains=request.GET['search'])
    Q_responsible_4 = Q(responsible__email__contains=request.GET['search'])
    Q_responsibles_1 = Q(responsibles__username__contains=request.GET['search'])
    Q_responsibles_2 = Q(responsibles__first_name__contains=request.GET['search'])
    Q_responsibles_3 = Q(responsibles__last_name__contains=request.GET['search'])
    Q_responsibles_4 = Q(responsibles__email__contains=request.GET['search'])
    data = {}
    project = Project.objects.get(id=request.GET['project_id'])
    if request.GET['search'].isdigit():
        sprint = project.sprint_set.filter(
            Q_name |
            Q_created_1 |
            Q_created_2 |
            Q_created_3 |
            Q_created_4 |
            Q_description |
            Q_number |
            Q_responsible_1 |
            Q_responsible_2 |
            Q_responsible_3 |
            Q_responsible_4
        )
        issue = project.issue_set.filter(
            Q_name |
            Q_created_1 |
            Q_created_2 |
            Q_created_3 |
            Q_created_4 |
            Q_responsible_1 |
            Q_responsible_2 |
            Q_responsible_3 |
            Q_responsible_4 |
            Q_body |
            Q_number
        )
        userstory = UserStory.objects.filter(
            Q_name |
            Q_created_1 |
            Q_created_2 |
            Q_created_3 |
            Q_created_4 |
            Q_responsibles_1 |
            Q_responsibles_2 |
            Q_responsibles_3 |
            Q_responsibles_4 |
            Q_description |
            Q_number,
            sprint__project__id=request.GET['project_id']
        )
        task = Task.objects.filter(
            Q_name |
            Q_created_1 |
            Q_created_2 |
            Q_created_3 |
            Q_created_4 |
            Q_responsible_1 |
            Q_responsible_2 |
            Q_responsible_3 |
            Q_responsible_4 |
            Q_description |
            Q_number,
            user_story__sprint__project__id=request.GET['project_id']
        )
    else:
        sprint = project.sprint_set.filter(
            Q_name |
            Q_created_1 |
            Q_created_2 |
            Q_created_3 |
            Q_created_4 |
            Q_description |
            Q_responsible_1 |
            Q_responsible_2 |
            Q_responsible_3 |
            Q_responsible_4
        )
        issue = project.issue_set.filter(
            Q_name |
            Q_created_1 |
            Q_created_2 |
            Q_created_3 |
            Q_created_4 |
            Q_responsible_1 |
            Q_responsible_2 |
            Q_responsible_3 |
            Q_responsible_4 |
            Q_body
        )
        userstory = UserStory.objects.filter(
            Q_name |
            Q_created_1 |
            Q_created_2 |
            Q_created_3 |
            Q_created_4 |
            Q_responsibles_1 |
            Q_responsibles_2 |
            Q_responsibles_3 |
            Q_responsibles_4 |
            Q_description,
            sprint__project__id=request.GET['project_id']
        )
        task = Task.objects.filter(
            Q_name |
            Q_created_1 |
            Q_created_2 |
            Q_created_3 |
            Q_created_4 |
            Q_responsible_1 |
            Q_responsible_2 |
            Q_responsible_3 |
            Q_responsible_4 |
            Q_description,
            user_story__sprint__project__id=request.GET['project_id']
        )
    data['sprint'] = sprint
    data['issue'] = issue
    data['userstory'] = userstory
    data['task'] = task
    return data



def create_user(data):# функция регистрации пользователя
    try:
        user = User.objects.filter(email=data["email"]).exists()
        if user != True:
            user = User.objects.create_user(
                username=data["username"],
                password=data["password"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
            project = Project.objects.get(id=data['project_id'])
            project.members.add(user)
            return user
        else:
            return None
    except KeyError:
        try:
            token_mail = TokenEmail.objects.get(token=data['token'])
            user = User.objects.create_user(
                username=data["username"],
                password=data["password"],
                email=token_mail.email,
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
            project = token_mail.project
            project.members.add(user)
            TokenEmail.objects.get(token=data['token']).delete()
        except ObjectDoesNotExist:
            return None




def add_project(data):
    project = CreateProjectForm(data)
    if project.is_valid():
        return project.save()
    else:
        return None


def add_project_api(data):
    project = Project.objects.create(
        admin=data['admin'],
        name=data['name'],
        description=data['description'],
    )
    project.members.add(*data['members'])
    project.save()
    return project



def send_invit(data):
    key = str(uuid.uuid4())
    tokenemail = TokenEmail()
    tokenemail.email = data['email']
    tokenemail.token = key
    tokenemail.project = Project.objects.get(id=data['project'][0])
    tokenemail.save()
    if data['web']:
        send_mail(
                'Приглашение на регистрацию',
                'Перейдите по этой ссылке http://localhost/management/emailconfirmation?key={0} для регистрации '.format(tokenemail.token),
                'xventrisx@ukr.net',
                [tokenemail.email],
            )
        return tokenemail.token


def send_anvite_api(data):
    key = str(uuid.uuid4())
    tokenemail = TokenEmail()
    tokenemail.email = data['email']
    tokenemail.token = key
    tokenemail.project = Project.objects.get(id=data['project_id'])
    tokenemail.save()
    return key


def project_information(id):
    project = Project.objects.get(id=id)
    sprint = project.sprint_set.all()
    data = {
        'project': project,
        'sprint': sprint,
    }
    return data




def add_sprint(user, data):
    project = Project.objects.get(id=data['project_id'])
    sprint = Sprint()
    sprint.project = project
    sprint.created_by = user
    if isinstance(data['responsible'], str):
        sprint.responsible = User.objects.get(id=data['responsible'])
    elif not isinstance(data['responsible'], str):
        sprint.responsible = data['responsible']
    sprint.name = data['name']
    sprint.description = data['description']
    if isinstance(data['status'], str):
        sprint.status = SprintStatus.objects.get(alies__exact=data['status'])
    elif not isinstance(data['status'], str):
        sprint.status = data['status']
    counter = Counter(project, sprint)
    data = counter.set_count()
    return data


def add_userstory_for_sprint(user, data):
    try:
        sprint = Sprint.objects.get(id=data['sprint_id'])
        userstory = CreateUserStoryForm(data)
        if userstory.is_valid():
            userstory.instance.created_by = user
            userstory.instance.sprint = sprint
            project = sprint.project
            counter = Counter(project, userstory.instance)
            data = counter.set_count()
            return userstory.instance
        else:
            return None
    except KeyError:
        userstory = UserStory()
        userstory.name = data['name']
        userstory.created_by = user
        userstory.status = data['status']
        userstory.description = data['description']
        userstory.sprint = data['sprint']
        project = data['sprint'].project
        counter = Counter(project, userstory)
        userstory = counter.set_count()
        userstory.responsibles.add(*data['responsibles'])
        return userstory





def add_issue(user, data):
    project = Project.objects.get(id=data['project_id'])
    issue = Issue()
    if isinstance(data['status'], str):
        status = IssueStatus.objects.get(alies__exact=data['status'])
    if not isinstance(data['status'], str):
        issue.status = status
    issue.name = data['name']
    issue.created_by = user
    if isinstance(data['responsible'], str):
        issue.responsible = User.objects.get(id=data['responsible'])
    if not isinstance(data['responsible'], str):
        issue.responsible = data['responsible']
    issue.body = data['body']
    issue.project = project
    counter = Counter(project, issue)
    data = counter.set_count()
    return data


def add_task_for_userstory(user, data):
    try:
        user_story = UserStory.objects.get(id=data['userstory_id'])
        task = CreateTaskForm(data)
        if task.is_valid():
            task.instance.created_by = user
            task.instance.user_story = user_story
            project = user_story.sprint.project
            counter = Counter(project, task.instance)
            data = counter.set_count()
            return task.instance
        else:
            return None
    except KeyError:
        task = Task()
        task.name = data['name']
        task.created_by = user
        task.responsible = data['responsible']
        task.status = data['status']
        task.user_story = data['user_story']
        task.description = data['description']
        task.time_completion = data['time_completion']
        project = data['user_story'].sprint.project
        counter = Counter(project, task)
        task = counter.set_count()
        return task



def get_sprint(id):
    sprint = Sprint.objects.get(id=id)
    data = {
        'sprint': sprint
    }
    return data


def members_in_project(id):
    project = Project.objects.get(id=id)
    members = project.members.all()
    data = {
        'project': project,
        'members': members,
    }
    return data


def issues_for_project(id):
    project = Project.objects.get(id=id)
    issues = project.issue_set.all()
    data = {
        'project': project,
        'issues': issues,
    }
    return data


def two_list_issues(request, id):
    project = Project.objects.get(id=id)
    issues = project.issue_set.all()
    data = {
        'data': [],
    }
    for i in issues:
        para = []
        issue_stsus = StatusIssueForm(request.POST, instance=i)
        para.extend([i, issue_stsus])
        data['data'].append(para)
    return(data)



def get_issue(request, id):
    issue = Issue.objects.get(id=id)
    responsible_form = ChangeResponsibleForm(request.POST, instance=issue)
    issue_status = StatusIssueForm(request.POST, instance=issue)
    form_add_coment = CreateComentForm()
    data = {
        'issue': issue,
        'responsible_form': responsible_form,
        'issue_status': issue_status,
        'form_add_coment': form_add_coment,
    }
    return data


def user_inform(id):
    user = User.objects.get(id=id)
    data = {
        'user': user,
    }
    return data


def get_list_userstorys(id):
    print(id)
    sprint = Sprint.objects.get(id=id)
    list_userstorys = sprint.userstorys.all()
    data = {
        'list_userstorys': list_userstorys,
    }
    return data


def get_userstory(id):
    userstory = UserStory.objects.get(id=id)
    data = {
        'userstory': userstory,
    }
    return data


def get_list_task(id):
    userstory = UserStory.objects.get(id=id)
    tasks = userstory.tasks.all()
    data = {
        'tasks': tasks,
    }
    return data


def get_task(id):
    task = Task.objects.get(id=id)
    data = {
        'task': task,
    }
    return data



class ComentServis:
    def __init__(self, request, id):
        self.request = request
        self.id = id


    def get_coment_for_task(self):
        task = Task.objects.get(id=self.id)
        coments = task.coments.all()
        data = {
            'coments': coments,
        }
        return data


    def get_coment_for_sprint(self):
        sprint = Sprint.objects.get(id=self.id)
        coments = sprint.coments.all()
        data = {
            'coments': coments,
        }
        return data


    def get_coments_for_userstory(self):
        userstory = UserStory.objects.get(id=self.id)
        coments = userstory.coments.all()
        data = {
            'coments': coments,
        }
        return data


    def get_coments_for_issue(self):
        issue = Issue.objects.get(id=self.id)
        coments = issue.coments.all()
        data = {
            'coments':coments,
        }
        return data

    
    def set_coment_for_sprint(self):
        sprint = Sprint.objects.get(id=self.request.POST['sprint_id'])
        coment = Coment()
        coment.created_by = self.request.user
        coment.sprint = sprint
        coment.body = self.request.POST['body']
        coment.save()
        return coment


    def set_coment_for_userstory(self):
        userstory = UserStory.objects.get(id=self.request.POST['userstory_id'])
        coment = Coment()
        coment.created_by = self.request.user
        coment.userstories = userstory
        coment.body = self.request.POST['body']
        coment.save()
        return coment


    def set_coment_for_task(self):
        task = Task.objects.get(id=self.request.POST['task_id'])
        coment = Coment()
        coment.created_by = self.request.user
        coment.task = task
        coment.body = self.request.POST['body']
        coment.save()
        return coment


    def set_coment_fot_issue(self):
        issue =Issue.objects.get(id=self.request.POST['issue_id'])
        coment = Coment()
        coment.created_by = self.request.user
        coment.issue = issue
        coment.body = self.request.POST['body']
        coment.save()
        return coment


class Counter:
    def __init__(self, project, model):
        self.project = project
        self.model = model

    def set_count(self):
        self.model.number = self.project.count
        self.project.count += 1
        self.project.save()
        self.model.save()
        return self.model


class ComentServisAPI:
    def __init__(self, user, data):
        self.user = user
        self.data = data


    def set_coment_for_spint_api(self):
        coment = Coment()
        coment.created_by = self.user
        coment.sprint = self.data['sprint']
        coment.body = self.data['body']
        coment.save()
        return coment


    def set_coment_for_userstory_api(self):
        coment = Coment()
        coment.created_by = self.user
        coment.userstories = self.data['userstories']
        coment.body = self.data['body']
        coment.save()
        return coment


    def set_coment_for_task_api(self):
        coment = Coment()
        coment.created_by = self.user
        coment.task = self.data['task']
        coment.body = self.data['body']
        coment.save()
        return coment


