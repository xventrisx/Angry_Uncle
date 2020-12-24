from rest_framework.test import APIClient, APITestCase
from management.models.tokenemail import *
from tasker.models.sprint import *
from tasker.models.project import *
from tasker.models.userstory import *
from tasker.models.issue import *
from tasker.models.coment import *
from tasker.models.task import *
from django.contrib.auth.models import User
from management.services import *
from django.http import QueryDict
import uuid
from django.urls import reverse


class JwtTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )

    def test_get_jwt_token(self):
        URL = reverse('get_token')
        data = dict(
            username='TestUser',
            password='TestPassword',
        )
        client = APIClient()
        result = client.post(URL, data)
        self.assertTrue(isinstance(result.json(), dict))

    def test_refresh_token(self):
        URL_get_token = reverse('get_token')
        data = dict(
            username='TestUser',
            password='TestPassword',
        )
        client = APIClient()
        result = client.post(URL_get_token, data)
        refresh_url = reverse('refresh-token')
        data = dict(
            refresh=result.data['refresh']
        )
        result = client.post(refresh_url, data)
        print(result.data)
        self.assertTrue(isinstance(result.data['access'], str))


class TestInvitAPI(APITestCase):
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
        tokenemail = TokenEmail.objects.create(
            token='test_token_key',
            email='testmail@ukr.net',
            project=project
        )

    def test_send_invit_api(self):
        URL = reverse('send-invit-api')
        data = dict(
            email='testmail@ukr.net',
            project_id='1',
        )
        client = APIClient()
        result = client.post(URL, data)
        self.assertTrue(isinstance(result.json(), dict))
        self.assertEqual(result.status_code, 200)

    def test_takes_invit(self):
        URL = reverse('takes-invit')
        data = dict(
            token='test_token_key',
            username='Test_User',
            password='TestPassword',
            first_name='Testname',
            last_name='TestLastName',
        )
        client = APIClient()
        result = client.post(URL, data, format='json')
        self.assertTrue(isinstance(result.json(), dict))
        self.assertEqual(result.status_code, 200)


class TestIssueAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Admin = User.objects.create_user(
            username='TestAdmin',
            password='TestPassword',
        )
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )
        project = Project.objects.create(
            admin=user,
            name="Test Project",
            description="Test Description",
        )
