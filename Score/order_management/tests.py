from django.urls import reverse
from rest_framework.test import APIClient, APITestCase, APIRequestFactory, RequestsClient
from django.contrib.auth.models import User
from .models.order import Product, Order, Score
import requests



class TestToken(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )


    def test_get_auth_token(self):
        URL = reverse('api_token_auth')
        data = dict(
            username='TestUser',
            password='TestPassword',
        )
        client = APIClient()
        result = client.post(URL, data)
        self.assertTrue(isinstance(result.json(), dict))


class TestListProduct(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )
        Product.objects.bulk_create([
            Product(name='Стол', price=1700),
            Product(name='Ручка', price=15.70),
            Product(name='Чайник', price=569),
            Product(name='Ноутбук', price=32000),
        ])



    def test_get_list_product(self):
        URL = reverse('api_token_auth')
        data = dict(
            username='TestUser',
            password='TestPassword',
        )
        client = APIClient()
        result = client.post(URL, data)
        URL = reverse('get_list_all_product')
        client.credentials(HTTP_AUTHORIZATION='Token ' + result.json()['token'])
        result_2 = client.get(URL)
        self.assertTrue(isinstance(result_2.json(), list))



class TestReceivingAnProduct(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )
        Product.objects.bulk_create([
            Product(name='Стол', price=2300),
            Product(name='Стол', price=1700),
            Product(name='Ручка', price=15.70),
            Product(name='Чайник', price=569),
            Product(name='Ноутбук', price=32000),
        ])



    def test_get_list_product(self):
        URL = reverse('api_token_auth')
        data = dict(
            username='TestUser',
            password='TestPassword',
        )
        client = APIClient()
        result = client.post(URL, data)
        URL = reverse('search_products')
        #client.credentials(HTTP_AUTHORIZATION='Token ' + result.json()['token'])
        data = {'name_product': 'Стол'}
        print(result.json())
        token = 'Token '+ result.json()['token']
        print(token)
        r = requests.get('http://localhost:8000'+URL, json=data, headers=dict(Authorization=token))
        print(r.request.headers)
        print(r.json())
        #self.assertTrue(isinstance(result_2.json(), list))


