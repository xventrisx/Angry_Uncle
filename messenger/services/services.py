__all__ = [
    'add_group',
    'get_contact_for_user',
    'ChatManager',
    'MessagManager',
]

from django.core.mail import send_mail
from django.db.models import QuerySet
from authentication.models.user import User
from authentication.models.password import Ticket
from .models.chat import *
from .models.message import *
from .models.contacts import *
import uuid
import typing
from .notisend import SMS
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def get_contact_for_user(
        user: typing.Optional[User]
) -> typing.Union[None, QuerySet]:
    '''
    The function returns the queryset of the user's contacts.
    '''
    try:
        user_contacts = user.contacts.members.all()
        return user_contacts
    except Contact.DoesNotExist:
        return None


def add_group(request):  # Функция создайот групу.
    group = Chat.objects.create(
        name=request.POST['name'],
        chat_type='G',
    )
    ChatParticipant.objects.create(
        user=request.user,
        chat=group,
        type='OWNER',
    )
    try:
        users = User.objects.filter(id__in=request.POST['users'])
        for x in users:
            chat_member = ChatParticipant.objects.create(
                user=x,
                chat=group,
                type='MEMBER'
            )
        return group
    except KeyError:
        return group


def create_link(**kwargs):
    if kwargs.get('web', False):
        link = '/web/link/chanel/{}'.format(kwargs['name_chanel'])
        return link
    elif kwargs.get('api', False):
        link = '/api/link/chanel/{}'.format(kwargs['name_chanel'])
        return link


class ChatManager:
    def __init__(self, user, dialog_id=None, companion_id=None):
        self.user = user
        self.dialog_id = dialog_id
        self.companion_id = companion_id

    def get_dialogs_user(self):  # функция возвращает все диалоги юзера
        dialogs = Chat.objects.filter(chat_type='D', chatparticipant__user=self.user)
        list_companion = []  # Список кортеджей собеседников, и количества новых сообщений в чате
        for x in dialogs:
            members = x.chatparticipant_set.all()
            companion = members.exclude(user=self.user).last()
            messages = x.message_set.all()
            count_newe_messages = 0
            for i in messages:
                try:
                    i.whoread_set.get(user=self.user)
                except WhoRead.DoesNotExist:
                    count_newe_messages += 1
            quantity_newe_messages = len(x.message_set.exclude(sender=self.user, whoread__user=self.user))
            list_companion.append((companion, quantity_newe_messages, count_newe_messages))
        return list_companion

    def get_gruops_user(self):
        groups_messages = []
        groups = Chat.objects.filter(chat_type='G', chatparticipant__user=self.user)
        for x in groups:
            count_messages = len(x.message_set.exclude(sender=self.user, whoread__user=self.user))
            groups_messages.append((x, count_messages))
        return groups_messages

    def get_channels_user(self):
        channels_publish = []
        channels = Chat.objects.filter(chat_type='CH', chatparticipant__user=self.user)
        for x in channels:
            count_messages = len(x.message_set.exclude(sender=self.user, whoread__user=self.user))
            channels_publish.append((x, count_messages))
        return channels_publish

    def get_or_create_dialog_with_user(self):
        companion = User.objects.get(id=self.companion_id)
        dialog = Chat.objects.filter(
            chat_type='D',
            chatparticipant__user=self.user,
        ).filter(
            chatparticipant__user=companion
        ).last()
        if isinstance(dialog, Chat):
            messages = dialog.message_set.all()
            result = dict(
                dialog_with=companion,
                dialog=dialog,
                messages=messages,
            )
            return result
        elif not isinstance(dialog, Chat):
            dialog = Chat(
                name='dialog',
                chat_type='D',
            )
            dialog.save()
            for x in range(2):
                if x == 0:
                    dialog_participant = ChatParticipant(
                        user=self.user,
                        chat=dialog,
                        type='MEMBER'
                    )
                    dialog_participant.save()
                else:
                    dialog_participant = ChatParticipant(
                        user=companion,
                        chat=dialog,
                        type='MEMBER'
                    )
                    dialog_participant.save()
            messages = dialog.message_set.all()
            result = dict(
                dialog_with=companion,
                dialog=dialog,
                messages=messages,
            )
        return result

    def create_channel(self, data=dict):
        self.data = data
        channel = Chat.objects.create(
            name=data['name'],
            chat_type='CH'
        )
        ChatParticipant.objects.create(
            user=self.user,
            chat=channel,
            type='OWNER',
        )
        if isinstance(data.get('users_id'), str):
            users = User.objects.filter(id__in=data.getlist('users_id'))
            for x in users:
                chat_participant = ChatParticipant.objects.create(
                    user=x,
                    chat=channel,
                    type='MEMBER',
                )
        return channel

    def get_channel(self, id):
        channel = Chat.objects.filter(id=id, chat_type='CH').last()
        return channel

    def get_dialog(self, id):
        dialog = Chat.objects.filter(id=id, chat_type='D').last()
        members = dialog.chatparticipant_set.all()
        companion = members.exclude(user=self.user).last()
        result = (
            dialog,
            companion,
        )
        return result

    def get_group(self, id):
        group = Chat.objects.filter(id=id, chat_type='D').last()
        return group


class MessagManager:
    def __init__(
            self, sender: typing.Optional[User],
            text_message: typing.Optional[str] = None,
            chat: typing.Union[int, str, Chat, None] = None,
    ):
        self.sender = sender
        self.text_message = text_message
        self.chat = chat

        # self.sender принимает в себя обект юзера.
        # self.text_message принимает текст сообщения.
        # self.chat может принимать id диалога, или сам обект диалога.

    def create_message(self):
        if isinstance(self.chat, str):
            chat = Chat.objects.get(id=self.chat)
            message = Message()
            message.sender = self.sender
            message.chat = chat
            message.text_message = self.text_message
            message.save()
        elif not isinstance(self.chat, str):
            message = Message()
            message.sender = self.sender
            message.chat = self.chat
            message.text_message = self.text_message
            message.save()
        return message


    def set_who_read(
            self,
            message,
    ):

        """
        set_who_read принимает в себя один аргумент, ето обэкт сообщения. возврашает обект True если имеется екземпляр модели
        WhoRead, если нет, он его создайот, и сохраняет в баз данных. Возвращает обект сохраньонный в базе данных.
        """

        self.message = message
        try:
            read = message.whoread_set.get(user=self.sender)
            return True
        except ObjectDoesNotExist:
            who_read = WhoRead(
                user=self.sender,
                message=self.message
            )
            who_read.save()
            return who_read

    def get_messages(self):

        """
        get_messages  возвращает кверисет всех сообщений связаных с обектом self.chat.
        """

        if isinstance(self.chat, str):
            chat = Chat.objects.get(id=self.chat)
            messages = chat.message_set.all()
            return messages
        elif not isinstance(self.chat, str):
            messages = self.chat.message_set.all()
            return messages
