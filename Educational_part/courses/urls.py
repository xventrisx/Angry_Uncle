from django.urls import path
from .views import *

urlpatterns = [
    path('list-courser/', CoursesListAPIview.as_view(), name='get_list_all_courses'),
    path('list-students/', StudentsListAPIview.as_view(), name='get_list_all_students'),
    path('info-course/<int:pk>/', CourseInfoAPIView.as_view(), name='get_info_for_course'),
    path('add-student-for-course/', AddStudentCoursAPIviews.as_view(), name='add-student-on-course'),
    path('delete-student-for-course/<int:pk>/', DeleteStudentCourseAPIviews.as_view(), name='delete-student-for-course'),
    path('download_student_report/<int:pk>/', DownloadFileFormatView.as_view(), name='student_report_in_cvs_format'),
    path('my/<int:pk>', TestView.as_view()),
]
