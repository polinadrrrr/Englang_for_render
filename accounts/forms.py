from django import forms
from django.contrib.auth.models import User
from . models import Profile, Goal


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        try:
            self.user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Invalid username')
        if not self.user.check_password(password):
            raise forms.ValidationError('Invalid password')
        return cleaned_data
    

class RegisterForm(forms.ModelForm):

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['email'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = { 'password': forms.PasswordInput() }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'about_me']
        labels = {
            'image': 'Изображение профиля',
            'about_me': 'О себе',
        }
        widgets = { 'image': forms.FileInput() }


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Логин',
            'email': 'Email',
        }


class GoalForm(forms.ModelForm):

    class Meta:
        model = Goal
        fields = ['name', 'description', 'done']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'done': 'Выполнено',
        }
        widgets = { 'done': forms.CheckboxInput() }
