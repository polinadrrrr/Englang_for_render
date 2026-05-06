from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import Scenario, Conversation, Message
from .forms import ScenarioForm

# Create your views here.

class ScenarioListView(ListView):
    model = Scenario
    template_name = 'chat/scenario_list.html'


@method_decorator(login_required, name="dispatch")
class CreateScenarioView(CreateView):
    model = Scenario
    form_class = ScenarioForm
    template_name = 'chat/scenario_form.html'
    success_url = reverse_lazy('scenario_list')