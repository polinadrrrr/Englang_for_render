from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile

# Create your models here.
class Quiz(models.Model):
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def question_count(self):
        return self.question_set.count()


class Question(models.Model):
    class type(models.TextChoices):
        single = 'single'
        multiple = 'multiple'
   
    name = models.CharField(max_length=350)
    type = models.CharField(max_length=8, choices=type.choices, default=type.single)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    explanation = models.CharField(max_length=550)

    def get_answers(self):
        if self.type == 'single':
            return self.answer_set.filter(is_correct=True).first()
        else:
            qs = self.answer_set.filter(is_correct=True).values()
            return [i.get('name') for i in qs]
    
    def already_completed(self, user):
        user_choices = user.choice_set.all()
        done = user_choices.filter(question=self)
        if done.exists():
            return True
        return False

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
