from django.shortcuts import render, redirect

from .models import Quiz, QuizQuestion, QuizAnswer
from .forms import QuizForm


# Create your views here.
def quiz_detail(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = quiz.quizquestion_set.all()

    if request.method == 'POST':
        forms = []
        for question in questions:
            form = QuizForm(request.POST, question=question)
            forms.append(form)
        if all(form.is_valid() for form in forms):
            return render(request, 'quiz_result.html')

    else:
        forms = [QuizForm(question=question) for question in questions]

    return render(request, 'quiz_detail.html', {
        'forms': forms, 'quiz': quiz, 'questions': questions
    })
