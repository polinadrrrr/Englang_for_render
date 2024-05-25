from django.db import models
from django.contrib.auth.models import User
from pytils.translit import slugify

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pictures', null=True, blank=True, default='profile_pictures/default.png')
    about_me = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    @staticmethod
    def get_profile(user: User):
        profile = Profile.objects.filter(user=user).first()
        if not profile:
            profile = Profile.objects.create(user=user)
        return profile


class Goal(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    done = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('-done', '-created_at')
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        unique_together = ('name', 'slug', 'profile')
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

