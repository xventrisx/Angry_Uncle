from django.urls import reverse
from django.db.models import Q
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
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
        group = Group.objects.create(
            name='Cashier',
        )
        permissions = Permission.objects.filter(
            Q(name='Can add order') |
            Q(name='Can change order') |
            Q(name='Can view product')
        )
        for permission in permissions:
            group.permissions.add(permission)
        user.groups.add(group)
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



class TestReceivingAnProducts(APITestCase):
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



    def test_get_search_products(self):
        URL = reverse('api_token_auth')
        data = dict(
            username='TestUser',
            password='TestPassword',
        )
        client = APIClient()
        result = client.post(URL, data)
        URL = reverse('search_products')
        client.credentials(HTTP_AUTHORIZATION='Token ' + result.json()['token'])
        dict_prod = {'name_product': 'Стол'}
        r = client.get(URL, dict_prod)
        self.assertTrue(isinstance(r.json(), list))



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

    def test_get_receiving_products(self):
        URL = reverse('api_token_auth')
        data = dict(
            username='TestUser',
            password='TestPassword',
        )
        client = APIClient()
        result = client.post(URL, data)
        client.credentials(HTTP_AUTHORIZATION='Token ' + result.json()['token'])
        id_prod = str(Product.objects.filter(name='Стол').last().id)
        URL = reverse('receiving_an_product', args=(id_prod))
        r = client.get(URL)
        self.assertTrue(isinstance(r.json(), dict))



class TestCreateOrder(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )
        group = Group.objects.create(
            name='Cashier',
        )
        permissions = Permission.objects.filter(
            Q(name='Can add order') |
            Q(name='Can change order') |
            Q(name='Can view product')
        )
        for permission in permissions:
            group.permissions.add(permission)
        user.groups.add(group)
        Product.objects.bulk_create([
            Product(name='Стол', price=2300),
            Product(name='Стол', price=1700),
            Product(name='Ручка', price=15.70),
            Product(name='Чайник', price=569),
            Product(name='Ноутбук', price=32000),
        ])

    def test_get_receiving_products(self):
        URL = reverse('api_token_auth')
        data = dict(
            username='TestUser',
            password='TestPassword',
        )
        client = APIClient()
        result = client.post(URL, data)
        client.credentials(HTTP_AUTHORIZATION='Token ' + result.json()['token'])
        id_prod = str(Product.objects.filter(name='Стол').last().id)
        dict_id_prod = {'product': id_prod}
        URL = reverse('create_order')
        r = client.post(URL, dict_id_prod)
        self.assertTrue(isinstance(r.json(), dict))
        self.assertTrue(r.json().get('product', False))
        self.assertTrue(r.json().get('quantity', False))
        self.assertTrue(r.json().get('date_created', False))
        self.assertTrue(r.json().get('cost', False))
        self.assertTrue(r.json().get('status', False))
        self.assertTrue(r.json().get('number', False))
        self.assertTrue(r.json().get('pk', False))


class TestUpdateStatusOrder(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )
        group = Group.objects.create(
            name='Cashier',
        )
        permissions = Permission.objects.filter(
            Q(name='Can add order') |
            Q(name='Can change order') |
            Q(name='Can view product')
        )
        for permission in permissions:
            group.permissions.add(permission)
        user.groups.add(group)
        Product.objects.bulk_create([
            Product(name='Стол', price=2300),
            Product(name='Стол', price=1700),
            Product(name='Ручка', price=15.70),
            Product(name='Чайник', price=569),
            Product(name='Ноутбук', price=32000),
        ])
        prod = Product.objects.filter(name='Стол').last()
        Order.objects.create(
            product=prod,
            quantity=1,
        )


    def test_uodate_order(self):
        URL = reverse('api_token_auth')
        data = dict(
            username='TestUser',
            password='TestPassword',
        )
        client = APIClient()
        result = client.post(URL, data)
        client.credentials(HTTP_AUTHORIZATION='Token ' + result.json()['token'])
        id_prod = str(Product.objects.filter(name='Стол').last().id)
        dict_id_prod = {'product': id_prod}
        URL = reverse('create_order')
        answer = client.post(URL, dict_id_prod)
        order_pk = {'pk': answer.json()['pk']}
        dict_order_ready = {'status': 'READY'}
        URL = reverse('update_status_order', kwargs=(order_pk))
        res = client.put(URL, dict_order_ready)
        self.assertTrue(isinstance(res.json(), dict))
        self.assertTrue(res.json().get('product', False))
        self.assertTrue(res.json().get('quantity', False))
        self.assertTrue(res.json().get('date_created', False))
        self.assertTrue(res.json().get('cost', False))
        self.assertTrue(res.json().get('status', False))
        self.assertTrue(res.json().get('number', False))
        self.assertTrue(res.json().get('pk', False))



class TestAcceptancePayment(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )
        user_shop_assistant = User.objects.create_user(
            username='TestUserShop_assistant',
            password='TestPassword',
        )
        group = Group.objects.create(
            name='Cashier',
        )
        permissions = Permission.objects.filter(
            Q(name='Can add order') |
            Q(name='Can change order') |
            Q(name='Can view product')
        )
        for permission in permissions:
            group.permissions.add(permission)
        user.groups.add(group)
        Product.objects.bulk_create([
            Product(name='Стол', price=2300),
            Product(name='Стол', price=1700),
            Product(name='Ручка', price=15.70),
            Product(name='Чайник', price=569),
            Product(name='Ноутбук', price=32000),
        ])
        product = Product.objects.get(name='Стол', price=1700)
        order = Order.objects.create(
            product=product,
            cashier=user,
            shop_assistant=user_shop_assistant,
            cost=product.price,
            status='P',
        )


    def test_acceptance_payment(self):
        URL = reverse('api_token_auth')
        data = dict(
            username='TestUser',
            password='TestPassword',
        )
        client = APIClient()
        result = client.post(URL, data)
        client.credentials(HTTP_AUTHORIZATION='Token ' + result.json()['token'])
        order = Order.objects.last()
        order_pk = {'pk': order.id}
        dict_dress_size = {'dress_size': str(order.cost)}
        URL = reverse('acceptance_of_payment', kwargs=(order_pk))
        res = client.post(URL, dict_dress_size)
        self.assertTrue(isinstance(res.json(), dict))
        self.assertTrue(res.json().get('product', False))
        self.assertTrue(res.json().get('order', False))
        self.assertTrue(res.json().get('date_created', False))
        self.assertTrue(res.json().get('payment_made', False))



class TestAcceptancePayment(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestUser',
            password='TestPassword',
        )
        user_shop_assistant = User.objects.create_user(
            username='TestUserShop_assistant',
            password='TestPassword',
        )
        group = Group.objects.create(
            name='Cashier',
        )
        permissions = Permission.objects.filter(
            Q(name='Can add order') |
            Q(name='Can change order') |
            Q(name='Can view product')
        )
        for permission in permissions:
            group.permissions.add(permission)
        user.groups.add(group)
        Product.objects.bulk_create([
            Product(name='Стол', price=2300),
            Product(name='Стол', price=1700),
            Product(name='Ручка', price=15.70),
            Product(name='Чайник', price=569),
            Product(name='Ноутбук', price=32000),
        ])
        product = Product.objects.get(name='Стол', price=1700)
        order = Order.objects.create(
            product=product,
            cashier=user,
            shop_assistant=user_shop_assistant,
            cost=product.price,
            status='P',
        )