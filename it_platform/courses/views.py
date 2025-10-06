# courses/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Enrollment
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()  # queryset аныктоо
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()  # queryset аныктоо
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()  # queryset аныктоо
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Фильтрлөө логикасы
        return self.queryset.filter(student=self.request.user)