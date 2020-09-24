from django.contrib import admin
from .models.issue import *
from .models.coment import *
from .models.project import *
from .models.sprint import *
from .models.task import *
from .models.userstory import *

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Task)
admin.site.register(Sprint)
admin.site.register(UserStory)
admin.site.register(UserStoryStatus)
admin.site.register(Coment)
admin.site.register(SprintStatus)
admin.site.register(StatusTask)
admin.site.register(IssueStatus)