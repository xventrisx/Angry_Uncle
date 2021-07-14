__all__ = [
    'OrderSerializer',
    'ProductSerializer',
    'OrderUpdateStatusSerializer',
    'ScoreSerializer',
]

from rest_framework import serializers
from django.contrib.auth.models import User
from order_management.models.order import Product, Order, Score
from datetime import datetime, date, timedelta
from django.dispatch import Signal

create_order_signal = Signal()
change_status_order_signal = Signal()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'id'
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'product',
            'quantity',
            'cashier',
            'shop_assistant',
            'date_created',
            'cost',
            'status',
            'number',
            'pk',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        date_difference = date.today() - product.date_created
        order = Order(
            product=product,
            cashier=user,
            status='P',
        )
        order.cost = product.price
        last_order = Order.objects.last()
        if last_order:
            order.number = last_order.number + 1
        if date_difference.days > 30:
            amount_discount = product.price * 0.2
            discount_price = product.price - amount_discount
            order.cost = discount_price
        order.save()
        create_order_signal.send(sender=order)
        return order

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.shop_assistant = validated_data.get('shop_assistant', instance.shop_assistant)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.status = validated_data.get('status', instance.status)
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        change_status_order_signal.send(sender=instance)
        return instance


class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'status',
        ]


class ScoreSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Score
        fields = [
            'product',
            'order',
            'date_created',
            'payment_made',
        ]

    def create(self, validated_data):
        order = Order.objects.get(pk=self.context['view'].kwargs['pk'])
        if order.cost == float(self.context['request']._full_data['dress_size'].replace(',', '.')):
            score = Score(
                product=order.product,
                order=order,
                payment_made=float(self.context['request']._full_data['dress_size'].replace(',', '.')),
            )
            score.save()
            order.status = 'PAID'
            order.save()
            return score
