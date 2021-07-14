from django.db import models
from authentication.models.user import User

CHAT_TYPE = (
    ('D', 'dialog'),
    ('G', 'group'),
    ('CH', 'channel'),
)

PARTICIPANT_TYPE = (
    ('OWNER', 'Владелец'),
    ('ADMIN', 'Администратор'),
    ('MEMBER', 'Учасник'),
)


class Chat(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    chat_type = models.CharField(max_length=2, choices=CHAT_TYPE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}, {1}, {2}".format(self.name, self.chat_type, self.date_created)


class ChatParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    type = models.CharField(max_length=6, choices=PARTICIPANT_TYPE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.user, self.chat, self.type, self.date_created)
