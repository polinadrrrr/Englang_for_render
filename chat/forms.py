from django import forms
from .models import Scenario, Conversation, Message


class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = ['title', 'description', 'system_prompt', 'icon', 'is_active']
        labels = {
            'title': 'Название',
            'description': 'Краткое описание',
            'system_prompt': 'Инструкция для ИИ',
            'icon': 'Иконка',
            'is_active': 'Опубликовано',
        }
        widgets = {'system_prompt': forms.Textarea()}