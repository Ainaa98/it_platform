from rest_framework import serializers
from .models import Course, Lesson, Enrollment
from users.serializers import UserSerializer



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'content', 'video_url', 'order',
            'duration_minutes', 'is_published', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    lessons_count = serializers.SerializerMethodField()
    enrolled_students_count = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'level', 'price', 'duration_hours',
            'image', 'is_active', 'is_free', 'author', 'created_at', 'updated_at',
            'lessons_count', 'enrolled_students_count', 'is_enrolled'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_enrolled_students_count(self, obj):
        return obj.enrollments.count()

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.enrollments.filter(student=request.user).exists()
        return False

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CourseDetailSerializer(CourseSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['lessons']


class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'enrolled_at',
            'completed', 'completed_at'
        ]
        read_only_fields = ['id', 'student', 'enrolled_at', 'completed_at']

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)