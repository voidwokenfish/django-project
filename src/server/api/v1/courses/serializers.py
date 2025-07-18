from rest_framework import serializers

from server.api.v1.users.serializers import UserListSerializer
from server.apps.courses.models import (Course, Enrollment, Lesson, Module,
                                        Topic)


class TopicSerializer(serializers.ModelSerializer):
    """Сериализатор для тем"""

    class Meta:
        model = Topic
        fields = ['id', 'title']


class CourseListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка курсов"""

    class Meta:
        model = Course
        fields = [
            "id", "title", "image", "price"
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра одного курса"""

    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения)))"""

    # topics = serializers.ManyRelatedField(many=True, read_only=True)
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'image',
            'price',
            'is_linear',
            'topics'
        ]


class ModuleListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка модулей"""

    class Meta:
        model = Module
        fields = [
            "id", "title", "course"
        ]


class ModuleDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра одного модуля"""

    course = CourseDetailSerializer(read_only=True)

    class Meta:
        model = Module
        fields = "__all__"


class ModuleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения модуля"""

    class Meta:
        model = Module
        fields = "__all__"


class LessonListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка уроков"""

    class Meta:
        model = Lesson
        fields = [
            "id", "title", "module"
        ]


class LessonDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра одного урока"""

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения урока"""

    class Meta:
        model = Lesson
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра зачислений на курс пользователей"""

    course = CourseListSerializer(read_only=True)
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'
