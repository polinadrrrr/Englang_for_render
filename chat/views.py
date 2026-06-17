from django.shortcuts import render, get_object_or_404, redirect
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
    model = Scenario # настроить по ролям
    template_name = 'chat/scenario_list.html'


@method_decorator(login_required, name="dispatch")
class ConversationListView(ListView):
    model = Conversation
    template_name = 'chat/conversation_list.html'

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)


@method_decorator(login_required, name="dispatch")
class CreateScenarioView(CreateView):
    model = Scenario
    form_class = ScenarioForm
    template_name = 'chat/scenario_form.html'
    success_url = reverse_lazy('scenario_list')


@method_decorator(login_required, name="dispatch")
class UpdateScenarioView(UpdateView):
    model = Scenario
    form_class = ScenarioForm
    template_name = 'chat/scenario_form.html'
    success_url = reverse_lazy('scenario_list')


@method_decorator(login_required, name="dispatch")
class DeleteScenarioView(DeleteView):
    model = Scenario
    template_name = 'delete.html'
    success_url = reverse_lazy('scenario_list')


@login_required
def start_conversation(request, scenario_slug):
    scenario = get_object_or_404(Scenario, slug=scenario_slug, is_active=True)
    conversation = Conversation.objects.create(
        user = request.user,
        scenario=scenario
    )
    return redirect('conversation', conversation_slug=conversation.slug)

@login_required
def conversation(request, conversation_slug):
    conversation = get_object_or_404(Conversation, slug=conversation_slug, user=request.user)
    messages = conversation.messages.all()
    context = {
        'conversation': conversation,
        'messages': messages,
        'scenario': conversation.scenario,
    }
    return render(request, 'chat/conversation.html', context)


