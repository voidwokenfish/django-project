from django import http
from django.shortcuts import render
from .models import Course, Module, Lesson
from django.views.generic import UpdateView
from django.urls import reverse


def index(request):
    courses = Course.objects.all()
    return render(request, 'index.html', context={"courses": courses})

def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    modules = course.module_set.all()
    return render(request, 'course_detail.html', context={"course": course, "modules": modules})

def module_detail(request, pk):
    module = Module.objects.get(pk=pk)
    lessons = module.lesson_set.all()
    return render(request, 'module_detail.html', context={"module": module, "lessons": lessons})

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
        pass

