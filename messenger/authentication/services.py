__all__ = [
    'create_user',
    'checkin',
    'web_authorization',
]

from django.db.models import QuerySet

from .models.user import User
from django.contrib.auth.hashers import make_password, is_password_usable, check_password
from django.contrib.auth import authenticate
from .models.password import Ticket
import typing
import uuid
from services.notisend import SMS
import phonenumbers

def create_user(
        data: typing.Optional[dict]
) -> typing.Union[User, None]:  # функция регистрации пользователя
    try:
        ticket = Ticket.objects.get(password=data['password_sms'])
        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
            email=data["email"],
            phone=ticket.number_phone
        )
        return user
    except Ticket.DoesNotExist:
        return None


def checkin(
        data: typing.Optional[dict]
) -> typing.Optional[bool]:  # Функция отправляет пользователю сообщение с кодом для подтверждения номера телифона.
    sms = SMS('Uzilis1019', '6c423a8a3c9b05522f655c14d47f5f9f')
    number_phone = phonenumbers.parse(data['phone'], "UA")
    if phonenumbers.is_valid_number(number_phone):
        key = str(uuid.uuid4()).split('-')
        ticket = Ticket()
        ticket.password = key[1]
        ticket.number_phone = data['phone']
        ticket.save()
        resalt_sms = sms.sendSMS(data['phone'], 'Код подтверждения, {}'.format(key[1]))
        return True
    else:
        return False


def web_authorization(
        data: typing.Optional[dict]
) -> typing.Union[bool, None, dict]:
    '''
    Checks the presence of the user in the database and the correctness of the password.
    Returns the processing result based on the received data.
    '''
    try:
        user = User.objects.get(phone=int(data['phone']))
    except User.DoesNotExist:
        return None
    else:
        user = authenticate(data, username=user.username, password=data.get('password'))
        if user is not None:
            return user
        else:
            return False
