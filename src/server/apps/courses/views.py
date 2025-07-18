from django import http
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Max
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView

from server.apps.courses.models import (Course, Enrollment, Lesson, Module,
                                        Topic, UserLessonCompleted)
from server.apps.quizzes.models import Quiz, QuizAttempt
from server.apps.transactions.models import Transaction
from server.apps.users.models import Profile
from server.services.payments.payment import PaymentService

User = get_user_model()


def index(request, topic_id=None, page_number=1):
    topic_id = request.GET.get('topic')
    page_number = request.GET.get('page', 1)
    topics = Topic.objects.all()
    if topic_id:
        courses = Course.objects.filter(topics=topic_id)
    else:
        courses = Course.objects.all()

    per_page = 12
    paginator = Paginator(courses, per_page)
    courses_paginator = paginator.page(page_number)

    user = request.user
    if user.is_authenticated:
        profile = user.profile


    return render(request, 'index.html', context={
        "courses": courses, "topics": topics, "courses_paginator": courses_paginator, "current_topic": topic_id, "profile": profile
    })

def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    modules = course.modules.all()

    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(course=course, user=request.user)
    else:
        enrolled = None

    return render(request, 'course_detail.html', context={
        "course": course, "modules": modules, "enrolled": enrolled
    })


def module_detail(request, pk):
    module = Module.objects.get(pk=pk)
    course = module.course

    lessons = list(module.lessons.all())
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

    progressbar = round((len(completed_lessons) + len(completed_quizzes)) / len(content_items) * 100)

    unlocked = True  # первый элемент всегда доступенн
    for item in content_items:
        if not course.is_linear:
            item["is_unlocked"] = True
            continue

        if unlocked:
            item["is_unlocked"] = True
        else:
            item["is_unlocked"] = False

        # Прверяем, завершен ли текущий элемент
        if item["type"] == "lesson" and item["obj"].id in completed_lessons:
            unlocked = True
        elif item["type"] == "quiz" and item["obj"].id in completed_quizzes:
            unlocked = True
        else:
            unlocked = False  # блокируем следующий, если текущий не завершен



    print(f" Прогресс = {progressbar}")

    return render(request, 'module_detail.html', {
        "module": module,
        "content_items": content_items,
        "completed_lessons": completed_lessons,
        "completed_quizzes": completed_quizzes,
        "progressbar": progressbar,
    })

def can_access_content(user, module, lessons, quizzes, items):
    """Проверяем открыт ли текущий урок или квиз для студента в линейном курсе.
    Если курс не линейный - доступ открыт по умолчанию.
    """
    if not module.course.is_linear:
        return True



def lesson_detail(request, pk):
    #Проверочку на прохождение урока
    lesson = Lesson.objects.get(pk=pk)
    module = Module.objects.get(pk=lesson.module.id)
    complition = UserLessonCompleted.objects.filter(
        user=request.user, lesson=lesson)

    return render(request, 'lesson_detail.html', context={
        "lesson": lesson, "complition": complition, "module": module
    })

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

# def enroll_student(request, pk):
#     if request.user.is_authenticated:
#         course = Course.objects.get(pk=pk)
#         Enrollment.objects.create(user=request.user, course=course, enroll_date=timezone.now().date())
#         return redirect('course_detail', pk=pk)
#     else:
#         return redirect('login')

@login_required
def enroll_student(request, pk):
    user = request.user
    course = Course.objects.get(id=pk)
    description = f"Оплата курса {course.title}"
    transaction = Transaction.objects.create(
        user=user,
        course=course,
        amount=course.price,
        description=description
    )
    url = PaymentService(transaction).execute()

    return redirect(url)

