from django import forms
from .models import Text, Word, Topic, Exercise


class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['name', 'theme', 'text_eng', 'text_rus', 'topic']
        labels = {
            'name': 'Название',
            'theme': 'Тема',
            'text_eng': 'Текст на английском', 
            'text_rus': 'Текст на русском',
            'topic': 'Топик',
        }


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['word_eng', 'word_rus', 'transcript']
        labels = {
            'word_eng': 'Слово на английском', 
            'word_rus': 'Слово на русском',
            'transcript': 'Транскрипция',
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'theme']
        labels = {
            'name': 'Название',
            'theme': 'Тема',
        }


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'theme', 'link']
        labels = {
            'name': 'Название',
            'theme': 'Тема',
            'link': 'Ссылка',
        }
