from django.contrib import admin
from django.urls import path
from . import views
from .models import Scenario, Conversation, Message

urlpatterns = [
    path('scenarios/', views.ScenarioListView.as_view(), name='scenario_list'),
    path('create_scenario/', views.CreateScenarioView.as_view(), name='create_scenario'),
    path('update_scenario/<slug:slug>/', views.UpdateScenarioView.as_view(), name='update_scenario'),
    path('delete_scenario/<slug:slug>/', views.DeleteScenarioView.as_view(), name='delete_scenario'),
    path('start/<str:scenario_slug>/', views.start_conversation, name='start_conversation'),
    path('conversation/<str:conversation_slug>', views.conversation, name='conversation'),
]