from django.db import models



class CourseParticipant(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.SET_NULL, related_name='course_participant', null=True,
                               blank=True)
    student = models.ForeignKey("courses.Student", on_delete=models.SET_NULL, related_name='course_student', null=True,
                                blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return '{0}, {1}, {2}'.format(
            self.course,
            self.student,
            self.completed
        )
