from django.contrib import admin
from .models.course import Course
from .models.student import Student
from .models.course_participant import CourseParticipant

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(CourseParticipant)
