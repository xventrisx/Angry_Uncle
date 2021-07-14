from django.contrib import admin
from .models.password import *
from .models.user import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = (
        'last_activity',
        'username',
    )
    search_fields = (
        'phone',
        'username',
        'last_activity',
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_filter = (
        'number_phone',
    )
    search_fields = (
        'number_phone',
    )

