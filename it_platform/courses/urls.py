from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')    # basename кошуу
router.register(r'lessons', LessonViewSet, basename='lessons')    # basename кошуу
router.register(r'enrollments', EnrollmentViewSet, basename='enrollments')  # basename кошуу

urlpatterns = [
    path('', include(router.urls)),
]