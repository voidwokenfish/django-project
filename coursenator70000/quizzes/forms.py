from .models import Quiz, QuizAnswer, QuizQuestion
from django import forms

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)

        self.fields['answer'] = forms.ChoiceField(
            choices=[(answer.id, answer.answer) for answer in question.quizanswer_set.all()],
            widget=forms.RadioSelect
        )