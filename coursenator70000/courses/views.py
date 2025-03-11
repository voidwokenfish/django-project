from django import http
from django.shortcuts import render
from .models import Course
from django.views.generic import UpdateView
from django.urls import reverse


def index(request):
    courses = Course.objects.all()
    return render(request, 'index.html', context={"courses": courses})

def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    return render(request, 'course_detail.html', context={"course": course})

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

