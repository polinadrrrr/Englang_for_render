from django.contrib import admin
from .models import Text, Word, Topic, Exercise

# Register your models here.
admin.site.register(Text)
admin.site.register(Word)
admin.site.register(Topic)
admin.site.register(Exercise)
