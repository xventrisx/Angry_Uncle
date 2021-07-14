from django.contrib import admin
from .models.chat import *
from .models.message import *
from .models.mentioning import *
from .models.contacts import *


@admin.register(Mentioning)
class MentioningAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'message',
        'date_created',
    )

    list_filter = (
        'user',
        'message',
        'date_created',
    )

    search_fields = (
        'user',
        'message',
        'date_created',
    )

    date_hierarchy = 'date_created'


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'chat_type',
        'date_created',
    )

    list_filter = (
        'name',
        'chat_type',
        'date_created',
    )

    search_fields = (
        'name',
        'chat_type',
        'date_created',
    )

    date_hierarchy = 'date_created'


@admin.register(ChatParticipant)
class ChatParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'chat',
        'type',
        'date_created',
    )

    list_filter = (
        'user',
        'chat',
        'type',
        'date_created',
    )

    search_fields = (
        'user',
        'chat',
        'type',
        'date_created',
    )

    date_hierarchy = 'date_created'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'sender',
        'chat',
        'date_created',
    )

    list_filter = (
        'sender',
        'chat',
        'date_created',
    )

    search_fields = (
        'sender',
        'chat',
        'date_created',
    )

    date_hierarchy = 'date_created'


@admin.register(WhoRead)
class WhoReadAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'message',
        'date_created',
    )

    list_filter = (
        'user',
        'message',
        'date_created',
    )

    search_fields = (
        'user',
        'message',
        'date_created',
    )

    date_hierarchy = 'date_created'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'whose',
    )

    list_filter = (
        'whose',
    )

    search_fields = (
        'whose',
        'members',
    )