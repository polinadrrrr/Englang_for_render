from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, render, redirect

from quizzes.models import Result
from .forms import LoginForm, RegisterForm, ProfileForm, UserForm, GoalForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from . models import Profile, Goal
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from theory.models import Lesson


# Create your views here.
class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('profile')
            else:
                context = {
                    'login_form': login_form,
                    'attention': f'Неверный логин или пароль'
                }
        else:
            context = {
                'login_form': login_form
            }
        return render(request, self.template_name, context)


class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get(self, request):
        user_form = RegisterForm()
        context = { 'user_form': user_form }
        return render(request, self.template_name, context)
    
    def post(self, request):
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('profile')
        context = { 'user_form': user_form }
        return render(request, self.template_name, context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('index')

def update_profile(request):
    user = request.user
    profile = Profile.get_profile(user)
    user_form = UserForm(instance=user)
    profile_form = ProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/update_profile.html', context)

def profiles(request):
    query = request.GET.get('q', '')
    goal = Goal.objects.filter(name__icontains=query)    
    # Создаем Q объекты для фильтрации
    name_filter = Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)
    username_filter = Q(user__username__icontains=query)
    email_filter = Q(user__email__icontains=query)
    about_filter = Q(about_me__icontains=query)
    goal_filter = Q(goal__in=goal)
    # Объединяем фильтры с помощью Q объектов
    search_filter = name_filter | username_filter | email_filter | about_filter | goal_filter
    # Фильтруем профили, исключая текущего пользователя и удаляя дубликаты
    object_list = Profile.objects.exclude(user=request.user).filter(search_filter).distinct()
    context = { 'object_list': object_list }
    return render(request, 'accounts/profiles.html', context)

@login_required(login_url=reverse_lazy('login'))
def user_profile_detail(request, username=None):
    if username:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    else:
        user = request.user
        profile = Profile.get_profile(user)
    goals = profile.goal_set.all().order_by('done', 'created_at')
    followers = profile.follows.all()
    three_days_ago = timezone.now() - timedelta(days=3)
    lessons_from_my_followers = Lesson.objects.filter(author__in=followers, published=True, created_at__gt=three_days_ago).order_by('-created_at')
    results = Result.objects.filter(user=user)
    total_quizzes = results.count()
    total_correct_answers = sum(result.correct_answers for result in results)
    total_wrong_answers = sum(result.wrong_answers for result in results)
    context = {
        'user': user,
        'profile': profile,
        'goals': goals,
        'followers': followers,
        'lessons': lessons_from_my_followers,
        'results': results,
        'total_quizzes': total_quizzes,
        'total_correct_answers': total_correct_answers,
        'total_wrong_answers': total_wrong_answers
    }
    if username:
        return render(request, 'accounts/user_profile_detail.html', context)
    else:
        return render(request, 'accounts/profile.html', context)

class AddGoalView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = 'accounts/goal_form.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        goal = form.save(commit=False)
        goal.profile = Profile.get_profile(self.request.user)
        try:
            goal.save()
        except IntegrityError:
            messages.error(self.request, 'Ошибка при добавлении цели. Возможно, такая цель уже существует.')
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем сообщения об ошибках в контекст
        context['messages'] = messages.get_messages(self.request)
        return context


class UpdateGoalView(LoginRequiredMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = 'accounts/goal_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        profile = Profile.get_profile(self.request.user)
        return profile.goal_set.get(slug=self.kwargs['goal_slug'])


class DeleteGoalView(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'delete.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        profile = Profile.get_profile(self.request.user)
        return profile.goal_set.get(slug=self.kwargs['goal_slug'])


class FollowUnfollowView(LoginRequiredMixin, View):
    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        current_profile = Profile.get_profile(request.user)
        action = request.POST.get('follow')
        if action == 'follow':
            current_profile.follows.add(profile)
        elif action == 'unfollow':
            current_profile.follows.remove(profile)
        current_profile.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



