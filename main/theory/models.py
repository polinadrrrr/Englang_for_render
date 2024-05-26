from django.db import models
from django.contrib.auth.models import User
from pytils.translit import slugify
from accounts.models import Profile
from tinymce.models import HTMLField
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Theme(models.Model):
    name = models.CharField('theme', max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        unique_together = ('name', 'slug')

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField('tag', max_length=100)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        unique_together = ('name', 'slug')

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)


class Lesson(models.Model):
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.CharField(max_length=200)
    content = HTMLField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_lessons', blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('published', '-created_at')
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        unique_together = ('name', 'slug', 'theme', 'content')
    
    def get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Lesson.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)

    def num_bookmarks(self):
        if self.bookmarks.count():
            return self.bookmarks.count()
        else:
            return '' or self.bookmarks.count()
    
    def num_comments(self):
        if self.comments.count():
            return self.comments.count()
        else:
            return '' or self.comments.count()


class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=5000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Parent comment')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.content

    def get_replies(self):
        return Comment.objects.filter(parent=self)


class Textbook(models.Model):
    author = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='textbooks/files/', blank=True)
    image = models.ImageField(upload_to='textbooks/img/', blank=True, default='textbooks/default.png')
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_textbooks', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Учебник'
        verbose_name_plural = 'Учебники'
        unique_together = ('name', 'slug')

    def get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Textbook.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)

    def num_bookmarks(self):
        if self.bookmarks.count():
            return self.bookmarks.count()
        else:
            return '' or self.bookmarks.count()


