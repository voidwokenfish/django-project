from rest_framework import serializers
from server.apps.courses.models import Course, Module, Lesson, Topic


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
        fields = ['title', 'description', 'image', 'price', 'is_linear', 'topics']