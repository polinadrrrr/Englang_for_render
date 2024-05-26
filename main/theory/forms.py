from django import forms
from .models import Theme, Lesson, Comment, Tag, Textbook
from tinymce.widgets import TinyMCE


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name', 'description']
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'description', 'theme', 'content', 'tags', 'published']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'theme': 'Тема',
            'content': 'Содержание',
            'tags': 'Теги',
            'published': 'Опубликовано',
        }
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'content': TinyMCE(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        labels = {'content': 'Текст комментария', 'parent': 'Родительский комментарий'}
        widgets = {'content': forms.Textarea()}


class TextbookForm(forms.ModelForm):
    class Meta:
        model = Textbook
        fields = ('name', 'theme', 'author', 'description', 'tags', 'file', 'image')
        labels = {
            'name': 'Название',
            'theme':'Тема',
            'author':'Автор',
            'description':'Описание',
            'tags':'Теги',
            'file':'Файл',
            'image':'Обложка',
        }
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'file': forms.FileInput(),
            'image': forms.FileInput(),
        }
