__all__ = [
    'StudentSerializer',
    'CoursesSerializer',
    'CourseParticipantSerializer',
    'CourseSerializer',
    'InfoCourseSerializer',
    'InfoStudentSerializer',
]

from rest_framework import serializers
from .models.course import Course
from .models.student import Student
from .models.course_participant import CourseParticipant


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'start_date',
            'end_date',
        ]


class CourseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseParticipant
        fields = [
            'id',
            'course',
            'student',
            'completed',
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'start_date',
            'end_date',
        ]


class InfoCourseSerializer(serializers.ModelSerializer):
    quantity_students = serializers.SerializerMethodField()
    first_ten_participants = serializers.SerializerMethodField()
    all_participants = serializers.SerializerMethodField()


    def get_quantity_students(self, obj):
        count = obj.course_participant.filter(course_id=obj.id).count()
        return count

    def get_first_ten_participants(self, obj):
        list_student = []
        first_ten_participants = obj.course_participant.filter(course_id=obj.id).order_by('-id')[:10]
        for participants in first_ten_participants:
            list_student.append(StudentSerializer(instance=participants.student).data)
        return list_student

    def get_all_participants(self, obj):
        list_participants = []
        all_participants = obj.course_participant.filter(course_id=obj.id)
        for participants in all_participants:
            list_participants.append(CourseParticipantSerializer(instance=participants).data)
        return list_participants

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'start_date',
            'end_date',
            'quantity_students',
            'first_ten_participants',
            'all_participants',
        ]


class InfoStudentSerializer(serializers.ModelSerializer):
    quantity_assigned_courses = serializers.SerializerMethodField()
    quantity_completed_courses = serializers.SerializerMethodField()

    def get_quantity_assigned_courses(self, obj):
        quantity_assigned_courses = obj.course_student.filter(completed=False).count()
        return quantity_assigned_courses


    def get_quantity_completed_courses(self, obj):
        quantity_completed_courses = obj.course_student.filter(completed=False).count()
        return quantity_completed_courses

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'quantity_assigned_courses',
            'quantity_completed_courses',
        ]