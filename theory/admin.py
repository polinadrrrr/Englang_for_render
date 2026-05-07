from django.contrib import admin
from .models import Theme, Lesson, Comment, Tag, Textbook

# Register your models here.
admin.site.register(Theme)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Textbook)