from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from pytils.translit import slugify


class Scenario(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    system_prompt = models.TextField(help_text="Системный промт для этого сценария")
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji или иконка")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    
    class Meta:
        ordering = ['title']
        verbose_name = 'Сценарий'
        verbose_name_plural = 'Сценарии'
        unique_together = ('title', 'slug')
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value)
        super().save(*args, **kwargs)

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='conversations')
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField()
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'
        unique_together = ('user', 'slug')

    def get_unique_slug(self):
        slug = slugify(f"{self.scenario} - {self.user.username} - {self.started_at}")
        unique_slug = slug
        num = 1
        while Conversation.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.slug}"

class Message(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
    
    def __str__(self):
        return f"{self.role}: {self.content[:20]}"