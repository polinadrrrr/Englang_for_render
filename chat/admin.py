from django.contrib import admin
from .models import Scenario, Conversation, Message

# Register your models here.
admin.site.register(Scenario)
admin.site.register(Conversation)
admin.site.register(Message)