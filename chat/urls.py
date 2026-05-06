from django.contrib import admin
from django.urls import path
from . import views
from .models import Scenario, Conversation, Message

urlpatterns = [
    path('scenarios/', views.ScenarioListView.as_view(), name='scenario_list'),
    path('create_scenario/', views.CreateScenarioView.as_view(), name='create_scenario'),
]