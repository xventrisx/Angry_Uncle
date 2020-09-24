from django.contrib import admin
from .models.tokenemail import *
from .models.profile import *


admin.site.register(TokenEmail)
admin.site.register(Profile)