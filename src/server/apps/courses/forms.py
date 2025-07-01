from django import forms


class CourseForm(forms.Form):
    title = forms.CharField(max_length=100, label="Название")
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField()
    is_linear = forms.BooleanField(required=False, label="Уведомить меня")

class LessonCompleteForm(forms.Form):
    pass

