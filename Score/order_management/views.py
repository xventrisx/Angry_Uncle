from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework import response as rest_response
from rest_framework import status as rest_status
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .serializers import *
from .permission import PermissionCashier, PermissionAccountant
from .models.order import Product, Order, Score
from datetime import date, datetime, timedelta
from django.dispatch import Signal
from django.contrib.auth.models import Group

create_order_signal = Signal()
change_status_order_signal = Signal()


class ListProductAPIView(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
        PermissionCashier,
    )
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return rest_response.Response(data=serializer.data, status=rest_status.HTTP_200_OK)


class ReceivingProductAPIView(generics.RetrieveAPIView):
    '''
        Тип запроса GET.
        Возвращает иформацию о продукте
        в вормате json.
    '''

    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Product.objects.all()


class CreateOrderAPIView(generics.CreateAPIView):
    '''
        Тип запроса POST.
        request.data должен содержать в себе ключи
        'name', 'price', 'id'.
        ключи хранят  под собой информацию о продукте,
        который есть в базе данных.
        Создайот обект заказа в базе данных,
        и оповещает продавца консультанта о поступление
        нового заказа.
        Возвращает информаци о заказе в формате json.
    '''

    permission_classes = (
        IsAuthenticated,
        PermissionCashier,
    )
    serializer_class = OrderSerializer





class UpdateStatusOrderAPIView(generics.UpdateAPIView):
    '''
        Тип запроса PUT.
        Запрос должен содержать в себе kwargs с ключом pk
        request.POST должен содержать ключ 'status'
        Обновляэт статус заказ,и оповещает касира о изменение статуса заказс
    '''

    permission_classes = (
        IsAuthenticated,
        PermissionCashier,
    )
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()


class AcceptancePaymentAPIView(generics.CreateAPIView):
    '''
        Тип запроса POST.
        request.POST содержит в себе клюс 'dress_size',
        с типом данних float().
        Создаёт обэкт Score, онже чек.
        Меняет статус заказ на оплачено.
        Возвращает информаци о Score в формате json.
    '''
    permission_classes = (
        IsAuthenticated,
        PermissionCashier,
    )
    serializer_class = ScoreSerializer




class SearchProductAPIView(generics.ListAPIView):
    '''
        Тип запроса GET.
        request.data должен содержать в себе ключ
        name_product
        Возвращает информацию о продукте, или продуктах в базе
        данныхв в формате JSON.
    '''
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.filter(name=self.request.query_params.get('name_product'))
        return products



class SearchOrderAPIView(generics.ListAPIView):
    '''
        Тип запроса GET.
        request.data должен содержать в себе ключи
        'date_start_search', 'date_finish_search'
        Возвращает информацию о заказах за периуд
        указаних дат в формате JSON.
    '''
    permission_classes = (
        IsAuthenticated,
        PermissionAccountant,
    )
    serializer_class = OrderSerializer

    def get_queryset(self):
        data_dict = {}
        for key, value in self.request.data.dict().items():
            list_data = value.split('.')
            list_data.reverse()
            str_value = '.'.join(list_data)
            value = datetime.strptime(str_value, "%Y.%m.%d")
            data_dict[key] = value.date()
        queryset = Order.objects.filter(date_created__gte=data_dict['date_start_search']).filter(
            date_created__lte=data_dict['date_finish_search'])
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return rest_response.Response(data=serializer.data, status=rest_status.HTTP_200_OK)
