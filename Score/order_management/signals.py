from django.dispatch import receiver
from django.core.mail import send_mail
from .views import create_order_signal, change_status_order_signal
from .models.order import Product, Order, Score
from django.contrib.auth.models import User

@receiver(create_order_signal)
def handler_create_order_signal(sender, **kwargs):
    shop_assistants = User.objects.filter(groups__name='Shop assistant')
    for shop_assistant in shop_assistants:
        send_mail('Создан новий зака',
            'Касир получил новый звказ. Обработайте заказ, и установите статус. Номер заказ {0}'.format(sender.number),
            'test_pochta@ukr.net',
            [shop_assistant.email])


@receiver(change_status_order_signal)
def handler_create_order_signal(sender, **kwargs):
    shop_assistants = User.objects.filter(groups__name='Shop assistant')
    for shop_assistant in shop_assistants:
        send_mail('Статус заказа обновльон',
            'Продавец-консультант {0} обраблотал заказ номер {1}, и обновил статус. Статус заказ на {2}'.format(
                sender.shop_assistant.username,
                sender.number,
                sender.get_status_display(),
            ),
            'test_pochta@ukr.net',
            [shop_assistant.email])