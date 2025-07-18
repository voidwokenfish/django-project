from rest_framework import serializers

from server.apps.quizzes.models import (Quiz, QuizAnswer, QuizAttempt,
                                        QuizQuestion)


class QuizAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответов от квизов"""

    class Meta:
        model = QuizAnswer
        fields = '__all__'



class SubmitAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    answer = serializers.IntegerField()


class QuizQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов квизов"""

    answers = QuizAnswerSerializer(many=True)

    class Meta:
        model = QuizQuestion
        fields = '__all__'


class QuizListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка квизов"""

    questions_count = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()


    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'number',
            'course_order',
            'pass_score',
            'is_complete_required',
            'questions_count',
            'answers_count'
        ]

    def get_questions_count(self, obj):
        return obj.questions.count()

    def get_answers_count(self, obj):
        return QuizAnswer.objects.filter(question__quiz=obj).count()


class QuizDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра одного квиза"""

    questions = QuizQuestionSerializer(many=True)
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = '__all__'

    def get_answers(self, obj):
        answers_qs = QuizAnswer.objects.filter(question__quiz=obj)
        return QuizAnswerSerializer(answers_qs, many=True).data


class QuizWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения квиза"""

    questions = QuizQuestionSerializer(many=True)
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = '__all__'

    def get_answers(self, obj):
        answers_qs = QuizAnswer.objects.filter(question__quiz=obj)
        return QuizAnswerSerializer(answers_qs, many=True).data
