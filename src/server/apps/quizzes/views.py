from datetime import date, timedelta

from django.db.models import Count
from django.shortcuts import redirect, render

from .models import Quiz, QuizAnswer, QuizAttempt, QuizQuestion


def quiz_detail(request, pk):
    request.session['quiz_id'] = pk
    module_id = request.GET.get('module_id')
    print(module_id)
    if module_id:
        request.session['module_id'] = module_id
    quiz = Quiz.objects.filter(pk=pk).annotate(questions_count=Count('quizquestion')).first()
    return render(request, 'quiz_detail.html', {
        'quiz': quiz, 'module_id': module_id
    })

def get_questions(request, is_start=False):

    module_id = request.session.get('module_id')

    if is_start:
        request = _reset_quiz(request)
        question = _get_first_question(request)
    else:
        question = _get_next_question(request)
        if question is None:
            return get_finish(request)

    answers = QuizAnswer.objects.filter(question=question)
    request.session['question_id'] = question.id

    return render(request, 'question.html',
                  {'question': question, 'answers': answers})

def _get_first_question(request):
    quiz_id = request.POST['quiz_id']
    return QuizQuestion.objects.filter(quiz_id=quiz_id).order_by('id').first()

def _get_next_question(request):
    quiz_id = request.POST['quiz_id']
    previous_question_id = request.session['question_id']

    try:
        return QuizQuestion.objects.filter(
            quiz_id=quiz_id, id__gt=previous_question_id
        ).order_by('id').first()
    except QuizQuestion.DoesNotExist:
        return None

def get_answer(request):
    chosen_answer_id = request.POST['answer_id']
    chosen_answer = QuizAnswer.objects.get(id=chosen_answer_id)
    print(f"Тип данных: {type(chosen_answer.is_correct)}")
    print(f"Значение: {chosen_answer.is_correct}")

    if chosen_answer.is_correct:
        correct_answer = chosen_answer
        request.session['score'] = request.session.get('score', 0) + 1
    else:
        correct_answer = QuizAnswer.objects.get(
            question_id=chosen_answer.question_id, is_correct=True
        )

    answer_type = type(chosen_answer.is_correct).__name__

    return render(request, 'answer.html', {
        'chosen_answer': chosen_answer,
        'answer': correct_answer,
        'answer_type': answer_type,
    })

def get_finish(request):
    quiz = QuizQuestion.objects.get(id=request.session['question_id']).quiz
    questions_count = QuizQuestion.objects.filter(quiz=quiz).count()
    score = request.session.get('score', 0)
    percent = int(score / questions_count * 100)
    _set_attempt_score(request, percent)
    request = _reset_quiz(request)

    module_id = request.session.get('module_id')
    if not module_id:
        return redirect('index')

    return render(request, 'finish.html', {
        'questions_count': questions_count,
        'score': score,
        'percent_score': percent,
        'module_id': module_id
    })

def _reset_quiz(request):
    if 'question_id' in request.session:
        del request.session['question_id']
    if 'score' in request.session:
        del request.session['score']
    return request

def _set_attempt_score(request, percent):

    quiz_id = request.session.get('quiz_id')
    user_id = request.user.id
    try:
        last_attempt = QuizAttempt.objects.get(quiz_id=quiz_id, user_id=user_id)
        if percent >= last_attempt.score:
            last_attempt.score = percent
            last_attempt.date = date.today()
        else:
            last_attempt.date = date.today()
    except QuizAttempt.DoesNotExist:
        last_attempt = QuizAttempt.objects.create(quiz_id=quiz_id, user_id=user_id, score=percent, date=date.today())

    last_attempt.save()
    return last_attempt


