__all__ = [
    'Product',
    'Order',
    'Score',
]

from django.db import models
from .staff import Staff
from django.contrib.auth.models import User


class Product(models.Model):
    '''
    Модель продукта описывает название товара,
    дату поступления в магазин,
    и стоимость товара.
    '''

    name = models.CharField(max_length=255)
    date_created = models.DateField(auto_now=True)
    price = models.FloatField()

    def __str__(self):
        return "{0}, {1}, {2},".format(
            self.name,
            self.date_created,
            self.price,
        )


STATUS_BUY = (
    ('P', 'В ОБРАБОТЕ'),
    ('PAID', 'ОПЛАЧЕН'),
    ('NO', 'ОТКЛОНЬОН'),
    ('READY', 'ГОТОВ К ВЫДАЧЕ')
)


class Order(models.Model):
    '''
    Модель заказа содержит информацию о продукте,
    касир получившем заказ,
    продавце-консультанте обработавший заказ,
    дата созданания заказа,
    стоимость заказа,
    и статус заказа.
    '''

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    shop_assistant = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='oreders', null=True, blank=True)
    date_created = models.DateField(auto_now=True)
    cost = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=5, choices=STATUS_BUY, null=True, blank=True)
    number = models.IntegerField(default=1)

    def __str__(self):
        return "{0}, {1}, {2}, {3}, {4}, {5}".format(
            self.product,
            self.cashier,
            self.shop_assistant,
            self.date_created,
            self.cost,
            self.status,
            self.number
        )


class Score(models.Model):
    '''
    Модель счета содержит информацию о прродукте,
    заказе, и дату создание счета.
    '''
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    date_created = models.DateField(auto_now=True)
    payment_made = models.FloatField(default=0)

    def __str__(self):
        return "{0}, {1}, {2}, {3},".format(
            self.product,
            self.order,
            self.date_created,
            self.payment_made,
        )
