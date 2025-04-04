from django.db.models import Max

from django.utils import timezone

from django import http
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.contrib.auth import get_user_model

from .models import Course, Module, Lesson, Enrollment, UserLessonCompleted
from django.views.generic import UpdateView
from django.urls import reverse

from quizzes.models import Quiz, QuizAttempt

User = get_user_model()


def index(request):
    courses = Course.objects.all()
    return render(request, 'index.html', context={"courses": courses})

def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    modules = course.module_set.all()
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(course=course, user=request.user).exists()
    else:
        enrolled = False
    return render(request, 'course_detail.html', context={"course": course, "modules": modules, "enrolled": enrolled})


def module_detail(request, pk):
    module = Module.objects.get(pk=pk)

    lessons = list(module.lesson_set.all())
    quizzes = list(Quiz.objects.filter(module=module))

    # Объединяем уроки и тесты, сортируя по course_order
    content_items = sorted(
        [{"type": "lesson", "obj": lesson} for lesson in lessons] +
        [{"type": "quiz", "obj": quiz} for quiz in quizzes],
        key=lambda x: x["obj"].course_order
    )

    completed_lessons = UserLessonCompleted.objects.filter(
        user=request.user, lesson__in=lessons
    ).values_list("lesson_id", flat=True)

    max_scores = QuizAttempt.objects.filter(user=request.user).values('quiz').annotate(
        max_score=Max('score'))
    user_scores = {item['quiz']: item['max_score'] for item in max_scores}
    completed_quizzes = {quiz.id for quiz in quizzes if user_scores.get(quiz.id, 0) >= quiz.pass_score}

    return render(request, 'module_detail.html', {
        "module": module,
        "content_items": content_items,
        "completed_lessons": completed_lessons,
        "completed_quizzes": completed_quizzes,
    })


def lesson_detail(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    return render(request, 'lesson_detail.html', context={"lesson": lesson})

class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'course_update.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('course_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.save()
        return http.HttpResponseRedirect(reverse('course_detail', kwargs={'pk': self.object.pk}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


def httptest(request):
    q = Course.objects.get(id=2)
    q2 = Course.objects.all()
    q3 = q2.first()
    q4 = Course.objects.in_bulk()
    print(q4)
    print(q3)
    print(q2.query) #Получить запрос
    print(q)
    print(q.price)
    return http.HttpResponse('test')

def enroll_student(request, pk):
    if request.user.is_authenticated:
        course = Course.objects.get(pk=pk)
        Enrollment.objects.create(user=request.user, course=course, enroll_date=timezone.now().date())
        return redirect('course_detail', pk=pk)
    else:
        return redirect('login')

def complete_lesson(request, pk):
    if request.user.is_authenticated:
        lesson = Lesson.objects.get(pk=pk)
        UserLessonCompleted.objects.create(
            user=request.user, lesson=lesson, completed_datetime=timezone.now().date()
        )
        module_id = lesson.module.id
        return redirect('module_detail', pk=module_id)
    else:
        return redirect('index')