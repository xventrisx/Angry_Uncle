from io import StringIO
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework import status as rest_status
from rest_framework.views import APIView
from rest_framework_csv.renderers import CSVRenderer
from .models.course import Course
from .models.student import Student
from .models.course_participant import CourseParticipant
from .serializers import *
from django.db.models import Count
from .services import PaginationStudent


class CoursesListAPIview(generics.ListAPIView):
    serializer_class = CoursesSerializer

    def get_queryset(self):
        return Course.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(data=serializer.data, status=rest_status.HTTP_200_OK)


class StudentsListAPIview(generics.ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(data=serializer.data, status=rest_status.HTTP_200_OK)


class AddStudentCoursAPIviews(generics.UpdateAPIView):
    serializer_class = CourseParticipantSerializer

    def put(self, request, *args, **kwargs):
        student = Student.objects.filter(id=self.request.data.get('id_student')).last()
        course = Course.objects.filter(id=self.request.data.get('id_course')).last()
        course_participant = CourseParticipant.objects.create(
            course=course,
            student=student,
        )
        serializer = self.serializer_class(course_participant)
        return Response(data=serializer.data, status=rest_status.HTTP_200_OK)


class DeleteStudentCourseAPIviews(generics.DestroyAPIView):
    lookup_field = 'pk'

    def get_queryset(self):
        return CourseParticipant.objects.all()


class CourseInfoAPIView(generics.RetrieveAPIView):
    serializer_class = InfoCourseSerializer

    def get(self, request, *args, **kwargs):
        try:
            instance = Course.objects.get(pk=kwargs.get('pk'))
            serializer = self.serializer_class(instance=instance, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DownloadFileFormatView(generics.RetrieveAPIView):

    def _download_csv(self, *args, **kwargs):
        import csv

        student = None
        try:
            student = Student.objects.get(id=kwargs.get('pk'))
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if student is not None:
            context = {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
                'appointment_courses': student.course_student.all().count(),
                'completed_courses': student.course_student.filter(completed=True).count(),
            }
            in_memory = StringIO()
            csv_filename = f"student_{student.id}.csv"
            w = csv.DictWriter(in_memory, fieldnames=list(context.keys()))
            w.writeheader()
            w.writerow(context)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f"attachment; filename={csv_filename}"
            in_memory.seek(0)
            response.write(in_memory.getvalue().encode('cp1251'))

            return response
        return Response({'message': ''}, status=status.HTTP_400_BAD_REQUEST)

    def _download_pdf(self, *args, **kwargs):
        import Pdf
        pass

    def _download_jpeg(self, *args, **kwargs):
        from PIL import PngImagePlugin
        pass

    def get(self, request, *args, **kwargs):
        return {"csv": self._download_csv, "pdf": self._download_pdf, "jpeg": self._download_jpeg}.get(
            request.query_params.get("format", "csv"))(*args, **kwargs)


class TestView(APIView):
    def get(self, request, *args, **kwargs):
        print(request.query_params.get("format", "csv"))
        return Response({"key": request.GET.get("format", "csv"), "pk": kwargs.get("pk", None)})
