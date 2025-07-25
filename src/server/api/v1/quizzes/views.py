from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from server.api.core.pagination.base import StandardPagePagination
from server.api.v1.quizzes.serializers import (QuizDetailSerializer,
                                               QuizListSerializer,
                                               QuizQuestionSerializer,
                                               QuizWriteSerializer,
                                               SubmitAnswerSerializer)
from server.apps.quizzes.models import (Quiz, QuizAnswer, QuizAttempt,
                                        QuizQuestion)


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.filter().order_by('id')
    serializer_class = QuizListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardPagePagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id', 'title', 'number', 'course_order')
    search_fields = ('title', 'id')

    def get_serializer_class(self):

        if self.action in ('create', 'update', 'partial_update'):
            return QuizWriteSerializer
        if self.action == 'retrieve':
            return QuizDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'], url_path='start')
    def start(self, request, pk=None):

        first_question = QuizQuestion.objects.select_related('quiz').filter(quiz_id=pk).order_by('id').first()
        serializer = QuizQuestionSerializer(first_question)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='answer')
    def sumbit_answer(self, request, pk=None):
        serializer = SubmitAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question_id = int(serializer.validated_data['question'])
        answer_id = int(serializer.validated_data['answer'])

        question = get_object_or_404(QuizQuestion, id=question_id, quiz_id=pk)
        answers = list(QuizAnswer.objects.filter(question=question))

        chosen_answer = next((a for a in answers if a.id == answer_id), None)
        correct_answer = next((a for a in answers if a.is_correct), None)

        if not chosen_answer:
            return Response({'detail': 'Ответ не найден'}, status=400)

        correct = (chosen_answer == correct_answer)

        return Response({
            'correct': correct,
            'correct_answer': correct_answer.id
        })

    @action(detail=True, methods=['post'], url_path='next')
    def next(self, request, pk=None):
        current_question_id = request.data.get('question')
        quiz = get_object_or_404(Quiz, id=pk)

        next_question = QuizQuestion.objects.filter(
            quiz=quiz, id__gt=current_question_id
        ).order_by('id').first()

        if next_question:
            return Response(QuizQuestionSerializer(next_question).data)
        else:
            return Response({'detail' : 'Вопросов больше нет.', 'flag' : 'quiz_finished'}, status=404)

    @action(detail=True, methods=['post'], url_path='finish')
    def finish(self, request, pk=None):

        user_id = request.user.id

        quiz = get_object_or_404(Quiz, id=pk)
        questions_count = QuizQuestion.objects.filter(quiz=quiz).count()

        score = int(request.data.get('score', 0))
        percent = score / questions_count * 100

        attempt, _ = QuizAttempt.objects.update_or_create(
            user_id=user_id, quiz_id=quiz.id,
            defaults={"score": score, 'date': date.today()}
        )

        return Response({
            'score' : score,
            'percent' : percent
        })







# class QuizAttemptViewSet(viewsets.ModelViewSet):
#     queryset = QuizAttempt.objects.filter().order_by('id')
#     serializer_class = QuizAttemptSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     pagination_class = StandardPagePagination
#     filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
#     ordering_fields = ('user', 'quiz', 'date', 'course_order')
#     search_fields = ('user', 'quiz')


# class QuizSubmitAnswerView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, quiz_id):
#         serializer = SubmitAnswerSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         question_id = serializer.validated_data['question']
#         answer_id = serializer.validated_data['answer']
#
#         question = get_object_or_404(QuizQuestion, id=question_id, quiz_id=quiz_id)
#         answer = get_object_or_404(QuizAnswer, id=answer_id, question=question)
#
#         if answer.is_correct:
#             correct = True
#         else:
#             correct = False
#             answer = QuizAnswer.objects.get(question=question, is_correct=True)
#
#         return Response({
#             'correct': correct,
#             'correct_answer': answer.id
#         })