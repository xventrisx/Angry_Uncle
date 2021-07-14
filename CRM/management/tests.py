from django.test import TestCase
from django.test import Client
from tasker.models.sprint import *
from tasker.models.project import *
from tasker.models.userstory import *
from tasker.models.issue import *
from tasker.models.coment import *
from tasker.models.task import *
from management.forms import *
from django.contrib.auth.models import User
from management.services import *
from django.http import QueryDict
import uuid


class ProjectsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )
        user_two = User.objects.create_user(
            username='TestUserTwo',
            password='TestPasswordTwo',
        )
        project = Project.objects.create(
            admin=user,
            name="Test Project",
            description="Test Description",
        )
        project.members.add(user, user_two)

    def test_project_web(self):
        user = User.objects.get(id=1)
        data = QueryDict(mutable=True)
        data['admin'] = user.id
        data['name'] = 'Test'
        data['description'] = 'Toje test'
        data['members'] = user.id
        result = add_project(data)
        self.assertTrue(result)

    def test_add_project_api(self):
        members = []
        for x in range(0, 3):
            lists = str(uuid.uuid4()).split('-')
            user = User.objects.create_user(
                username='TestUser' + lists[0],
                password=lists[-1],
            )
            members.append(user)
        data = QueryDict(mutable=True)
        data['admin'] = members[0]
        data['name'] = 'Test'
        data['description'] = 'Toje test'
        data['members'] = members
        result = add_project_api(data)
        self.assertTrue(result)

    def test_project_information(self):
        result = project_information(id=1)
        self.assertTrue(result['project'])
        if len(result['sprint']) > 0:
            self.assertTrue(result['project'])
            self.assertTrue(result['sprint'])
        self.assertTrue(result['project'])

    def test_members_in_projec(self):
        result = members_in_project('1')
        for x in result['members']:
            self.assertTrue(isinstance(x, User))
        self.assertTrue(isinstance(result['project'], Project))


class InvitTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )
        project = Project.objects.create(
            admin=user,
            name="Test Project",
            description="Test Description",
        )
        project.members.add(user)

    def test_send_invit(self):
        project = Project.objects.get(id=1)
        data = QueryDict(mutable=True)
        data['email'] = 'xxxxx@.com'
        data['project'] = [project.id]
        data['web'] = True
        result = send_invit(data)
        self.assertTrue(result)

    def test_send_invit_api(self):
        project = Project.objects.get(id=1)
        data = QueryDict(mutable=True)
        data['email'] = 'xxxxx@.com'
        data['project_id'] = project.id
        data['web'] = False
        result = send_anvite_api(data)
        self.assertTrue(result)


class SprintTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Admin = User.objects.create_user(
            username='TestAdmin',
            password='TestPassword'
        )
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword'
        )
        project = Project.objects.create(
            admin=Admin,
            name="Test Project",
            description="Test Description",
        )
        sprintststus = SprintStatus.objects.create(
            alies='Тест',
            name='Тестируется'
        )
        Sprint.objects.create(
            project=project,
            created_by=Admin,
            responsible=user,
            name='Test name sprint',
            description='Test description for sprint',
            status=sprintststus,
            number=project.count,
        )

    def test_add_sprint(self):
        user = User.objects.get(username='TestAdmin')
        data = QueryDict(mutable=True)
        data['project_id'] = '1'
        data['responsible'] = '2'
        data['name'] = 'Test name'
        data['description'] = 'Test description'
        data['status'] = 'Тест'
        result = add_sprint(user, data)
        self.assertTrue(isinstance(result, Sprint))

    def test_get_sprint(self):
        result = get_sprint('1')
        self.assertTrue(isinstance(result['sprint'], Sprint))


class UserstoryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Admin = User.objects.create_user(
            username='TestAdmin',
            password='TestPassword'
        )
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword'
        )
        user1 = User.objects.create_user(
            username='TestUser1',
            password='TestPassword'
        )
        project = Project.objects.create(
            admin=Admin,
            name="Test Project",
            description="Test Description",
        )
        sprintststus = SprintStatus.objects.create(
            alies='Тест',
            name='Тестируется'
        )
        sprint = Sprint.objects.create(
            project=project,
            created_by=Admin,
            responsible=user,
            name='Test name',
            description='Test description',
            status=sprintststus,
            number=project.count,
        )
        user_story_status = UserStoryStatus.objects.create(
            alies='Тест',
            name='Тестируется'
        )
        userstory = UserStory.objects.create(
            name='Test_userstory',
            created_by=user,
            status=user_story_status,
            description='Test_deskription',
            sprint=sprint,
            number=project.count
        )
        userstory.responsibles.add(user, user1)
        userstory.save()
        userstory_1 = UserStory.objects.create(
            name='Test_userstory_1',
            created_by=user1,
            status=user_story_status,
            description='Test_deskription',
            sprint=sprint,
            number=project.count
        )
        userstory_1.responsibles.add(user1, user)

    def test_add_userstory_for_sprint(self):
        user = User.objects.get(username='TestAdmin')
        data = dict()
        data['name'] = 'Тest userstory'
        data['responsibles'] = ['2', '3']
        data['status'] = 'Тест'
        data['description'] = 'Test description'
        data['sprint_id'] = '1'
        result = add_userstory_for_sprint(user, data)
        self.assertTrue(isinstance(result, UserStory))

    def test_get_list_userstorys(self):
        userstorys = get_list_userstorys(id=1)
        for x in userstorys['list_userstorys']:
            self.assertTrue(isinstance(x, UserStory))

    def test_get_userstory(self):
        userdtorys = UserStory.objects.all()
        userstory = get_userstory(id=userdtorys[0].id)
        self.assertTrue(isinstance(userstory['userstory'], UserStory))


class IssueTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Admin = User.objects.create_user(
            username='TestAdmin',
            password='TestPassword'
        )
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword'
        )
        user1 = User.objects.create_user(
            username='TestUser1',
            password='TestPassword'
        )
        project = Project.objects.create(
            admin=Admin,
            name="Test Project",
            description="Test Description",
        )
        isuue_status = IssueStatus.objects.create(
            alies='Тест',
            name='Тестируется'
        )
        iseeu = Issue.objects.create(
            name='Test issue',
            created_by=Admin,
            responsible=user,
            status=isuue_status,
            body='Test body',
            project=project,
            number=1,
        )

    def test_add_issue(self):
        user = User.objects.get(username='TestAdmin')
        data = {
            'name': 'Test issue',
            'responsible': '1',
            'status': 'Тест',
            'body': 'Test body',
            'project_id': '1',
        }
        result = add_issue(user, data)
        self.assertTrue(isinstance(result, Issue))

    def test_issues_for_project(self):
        result = issues_for_project('1')
        for x in result['issues']:
            self.assertTrue(isinstance(x, Issue))
        self.assertTrue(isinstance(result['project'], Project))

    def test_two_list_issues(self):
        data = QueryDict(mutable=True)
        result = two_list_issues(data, '1')
        for x in result['data']:
            self.assertTrue(isinstance(x[0], Issue))
            self.assertTrue(isinstance(x[1], StatusIssueForm))

    def test_get_issue(self):
        querydict = QueryDict(mutable=True)
        result = get_issue(querydict, '1')
        self.assertTrue(isinstance(result['issue'], Issue))
        self.assertTrue(isinstance(result['responsible_form'], ChangeResponsibleForm))
        self.assertTrue(isinstance(result['issue_status'], StatusIssueForm))
        self.assertTrue(isinstance(result['form_add_coment'], CreateComentForm))


class TaskTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        admin = User.objects.create_user(
            username='TestAdmin',
            password='TestPassword'
        )
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword'
        )
        user1 = User.objects.create_user(
            username='TestUser1',
            password='TestPassword'
        )
        project = Project.objects.create(
            admin=admin,
            name="Test Project",
            description="Test Description",
        )
        sprintststus = SprintStatus.objects.create(
            alies='Тест',
            name='Тестируется'
        )
        sprint = Sprint.objects.create(
            project=project,
            created_by=admin,
            responsible=user,
            name='Test name',
            description='Test description',
            status=sprintststus,
            number=project.count,
        )
        user_story_status = UserStoryStatus.objects.create(
            alies='Тест',
            name='Тестируется'
        )
        userstory = UserStory.objects.create(
            name='Тest userstory',
            created_by=admin,
            status=user_story_status,
            description='Test description',
            sprint=sprint,
            number=project.count,
        )
        userstory.responsibles.add(user, user1)
        status_task = StatusTask.objects.create(
            alies='Тест',
            name='Тестируется'
        )
        task_1 = Task.objects.create(
            name='Test task 1',
            created_by=admin,
            responsible=user,
            status=status_task,
            user_story=userstory,
            number=project.count
        )
        task_2 = Task.objects.create(
            name='Test task 1',
            created_by=admin,
            responsible=user1,
            status=status_task,
            user_story=userstory,
            number=project.count
        )

    def test_add_task_for_userstory(self):
        user = User.objects.get(username='TestAdmin')
        data = {
            'name': 'test task',
            'responsible': '2',
            'status': 'Тест',
            'description': 'ryeyh',
            'time_completion': '2021-05-01',
            'userstory_id': '1',
        }
        result = add_task_for_userstory(user, data)
        self.assertTrue(isinstance(result, Task))

    def test_get_list_task(self):
        userstory = UserStory.objects.all()
        tasks = get_list_task(id=userstory[0].id)
        for x in tasks['tasks']:
            self.assertTrue(isinstance(x, Task))

    def test_get_task(self):
        tasks = Task.objects.all()
        task = get_task(id=tasks[0].id)
        self.assertTrue(isinstance(task['task'], Task))


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword'
        )

    def user_inform(self):
        result = user_inform('1')
        self.assertTrue(isinstance(result['user'], User))


class CounterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        admin = User.objects.create_user(
            username='TestAdmin',
            password='TestPassword'
        )
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword'
        )
        user1 = User.objects.create_user(
            username='TestUser1',
            password='TestPassword'
        )
        project = Project.objects.create(
            admin=admin,
            name="Test Project",
            description="Test Description",
        )
        sprintststus = SprintStatus.objects.create(
            alies='Тест',
            name='Тестируется'
        )
        sprint = Sprint.objects.create(
            project=project,
            created_by=admin,
            responsible=user,
            name='Test name',
            description='Test description',
            status=sprintststus,
            number=project.count,
        )
        user_story_status = UserStoryStatus.objects.create(
            alies='Тест',
            name='Тестируется'
        )
        userstory = UserStory.objects.create(
            name='Тest userstory',
            created_by=admin,
            status=user_story_status,
            description='Test description',
            sprint=sprint,
            number=project.count,
        )
        userstory.responsibles.add(user, user1)
        status_task = StatusTask.objects.create(
            alies='Тест',
            name='Тестируется'
        )
        task_1 = Task.objects.create(
            name='Test task 1',
            created_by=admin,
            responsible=user,
            status=status_task,
            user_story=userstory,
            number=project.count
        )
        task_2 = Task.objects.create(
            name='Test task 1',
            created_by=admin,
            responsible=user1,
            status=status_task,
            user_story=userstory,
            number=project.count
        )

    def test_set_count(self):
        project = Project.objects.all().last()
        sprint = Sprint.objects.all().last()
        counter = Counter(
            project,
            sprint
        )
        result = counter.set_count()
        self.assertTrue(isinstance(result, Sprint))
