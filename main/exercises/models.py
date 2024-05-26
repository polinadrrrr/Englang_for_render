from django.db import models
from pytils.translit import slugify
from theory.models import Theme
from accounts.models import Profile
from django.contrib.auth.models import User

# Create your models here.
class Word(models.Model):
    word_eng = models.CharField('word', max_length=50)
    word_rus = models.CharField(max_length=50)
    transcript = models.CharField(max_length=50)
    
    def __str__(self):
        return self.word_eng + ' - ' + self.word_rus

    class Meta:
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'
        ordering = ('word_eng', 'word_rus')
        unique_together = ('word_eng', 'word_rus')


class Topic(models.Model):
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField('topic', max_length=100)
    slug = models.SlugField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, blank=True, null=True)
    words = models.ManyToManyField(Word, blank=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_topics', blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Топик'
        verbose_name_plural = 'Топики'
        unique_together = ('name', 'slug')
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)


class Text(models.Model):
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField('text', max_length=100)
    slug = models.SlugField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    text_eng = models.TextField()
    text_rus = models.TextField()
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_texts', blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'
        unique_together = ('name', 'slug')

    def get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Text.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)


class Exercise(models.Model):
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField('exercise', max_length=100)
    slug = models.SlugField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    link = models.URLField()
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_exercises', blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
        unique_together = ('name', 'slug')

    def get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Exercise.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{num}"
            num += 1
        return unique_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)
