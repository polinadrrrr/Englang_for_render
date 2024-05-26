from django import forms
from django.contrib.auth.models import User
from . models import Quiz, Question, Answer


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name']
        labels = {'name': 'Название теста'}


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'type', 'explanation']
        labels = {
            'name': 'Вопрос',
            'type': 'Тип вопроса',
            'explanation': 'Пояснение к вопросу',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['name', 'is_correct']
        labels = {
            'name': 'Ответ',
            'is_correct': 'Правильный',
        }
