from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from accounts.models import Profile
from .models import Text, Word, Topic, Exercise
from .forms import TextForm, WordForm, TopicForm, ExerciseForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import random

# Create your views here.
def topic_details(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    form = WordForm()
    search_words = None
    words = Word.objects.filter(topic=topic)
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            new_word = form.save(commit=False)
            new_word.topic = topic
            new_word.save()
            topic.words.add(new_word)
            form = WordForm()
            words = Word.objects.filter(topic=topic)
    if request.GET.get('q'):
        query = request.GET.get('q')
        search_words = Word.objects.distinct().filter(
            Q(word_eng__icontains=query) |
            Q(word_rus__icontains=query)
        )
    context = {
        'topic': topic, 
        'words': words,
        'search_words': search_words,
        'form': form
    }
    return render(request, 'exercises/topic_detail.html', context)


class TextDetail(DetailView):
    model = Text
    template_name = 'exercises/text_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.object.topic
        context['sentences'] = self.object.text_eng.split('. ')  # Разделение текста на предложения
        return context


class ExerciseDetail(DetailView):
    model = Exercise
    template_name = 'exercises/exercise_detail.html'


@method_decorator(login_required, name="dispatch")
class CreateTextView(CreateView):
    model = Text
    template_name = 'exercises/text_form.html'
    form_class = TextForm
    success_url = reverse_lazy('materials')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class CreateWordView(CreateView):
    model = Word
    template_name = 'exercises/word_form.html'
    form_class = WordForm
    success_url = reverse_lazy('materials')


@method_decorator(login_required, name="dispatch")
class CreateTopicView(CreateView):
    model = Topic
    template_name = 'exercises/topic_form.html'
    form_class = TopicForm
    success_url = reverse_lazy('materials')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class CreateExerciseView(CreateView):
    model = Exercise
    template_name = 'exercises/exercise_form.html'
    form_class = ExerciseForm
    success_url = reverse_lazy('materials')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class UpdateTextView(UpdateView):
    model = Text
    template_name = 'exercises/text_form.html'
    form_class = TextForm
    success_url = reverse_lazy('materials')


@method_decorator(login_required, name="dispatch")
class UpdateWordView(UpdateView):
    model = Word
    template_name = 'exercises/word_form.html'
    form_class = WordForm
    success_url = reverse_lazy('materials')


@method_decorator(login_required, name="dispatch")
class UpdateTopicView(UpdateView):
    model = Topic
    template_name = 'exercises/topic_form.html'
    form_class = TopicForm
    success_url = reverse_lazy('materials')


@method_decorator(login_required, name="dispatch")
class UpdateExerciseView(UpdateView):
    model = Exercise
    template_name = 'exercises/exercise_form.html'
    form_class = ExerciseForm
    success_url = reverse_lazy('materials')


@method_decorator(login_required, name="dispatch")
class DeleteTextView(DeleteView):
    model = Text
    template_name = 'delete.html'
    success_url = reverse_lazy('materials')


@method_decorator(login_required, name="dispatch")
class DeleteWordView(DeleteView):
    model = Word
    template_name = 'delete.html'
    success_url = reverse_lazy('materials')


@method_decorator(login_required, name="dispatch")
class DeleteTopicView(DeleteView):
    model = Topic
    template_name = 'delete.html'
    success_url = reverse_lazy('materials')


@method_decorator(login_required, name="dispatch")
class DeleteExerciseView(DeleteView):
    model = Exercise
    template_name = 'delete.html'
    success_url = reverse_lazy('materials')


@login_required
def add_word_to_topic(request, topic_slug, word_id):
    topic = get_object_or_404(Topic, slug=topic_slug)
    word = get_object_or_404(Word, id=word_id)
    topic.words.add(word)
    return redirect('topic_details', topic_slug=topic.slug)

@login_required
def remove_word_from_topic(request, topic_slug, word_id):
    topic = get_object_or_404(Topic, slug=topic_slug)
    word = get_object_or_404(Word, id=word_id)
    topic.words.remove(word)
    return redirect('topic_details', topic_slug=topic.slug)


class BookmarkObjectMixin:
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.object = self.get_object()
            if self.object.bookmarks.filter(id=request.user.id).exists():
                self.object.bookmarks.remove(request.user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                self.object.bookmarks.add(request.user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name="dispatch")
class BookmarkTextView(BookmarkObjectMixin, View):
    def get_object(self):
        return get_object_or_404(Text, id=self.kwargs.get('text_id'))


@method_decorator(login_required, name="dispatch")
class BookmarkTopicView(BookmarkObjectMixin, View):
    def get_object(self):
        return get_object_or_404(Topic, id=self.kwargs.get('topic_id'))


@login_required
def ten_random_words_from_bookmarks(request):
    topics = Topic.objects.filter(bookmarks__id=request.user.id)
    words = Word.objects.filter(topic__in=topics).order_by('?')[:10]
    context = {
        'object_list': words
    }
    return render(request, 'exercises/word_list.html', context)


class UserBookmarksMixin(View):
    model = None
    template_name = 'theory/materials.html'
    context_object_name = None

    def get_queryset(self):
        return self.model.objects.filter(bookmarks__in=[self.request.user])

    def get_context_data(self):
        context = {
            'profile': Profile.get_profile(self.request.user),
            self.context_object_name: self.get_queryset()
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    
class UserTextsBookmarksView(LoginRequiredMixin, UserBookmarksMixin):
    model = Text
    context_object_name = 'texts'

class UserTopicsBookmarksView(LoginRequiredMixin, UserBookmarksMixin):
    model = Topic
    context_object_name = 'topics'


class UserMaterialListView(LoginRequiredMixin, View):
    model = None  # Переопределяется в дочернем классе
    template_name = None  # Переопределяется в дочернем классе

    def get(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)
        materials = self.model.objects.filter(author=profile)
        context = {
            'profile': profile,
            'content': materials
        }
        return render(request, self.template_name, context)

class UserTextsView(UserMaterialListView):
    model = Text
    template_name = 'exercises/list_text.html'

class UserTopicsView(UserMaterialListView):
    model = Topic
    template_name = 'exercises/list_topic.html'

class UserExercisesView(UserMaterialListView):
    model = Exercise
    template_name = 'exercises/list_exercise.html'


class MaterialListView(LoginRequiredMixin, View):
    model = None  # Переопределяется в дочернем классе
    template_name = None  # Переопределяется в дочернем классе

    def get(self, request):
        profile = Profile.get_profile(request.user)
        materials = getattr(profile, f'{self.model}_set').all()
        context = {
            'content': materials,
            'profile': profile
        }
        return render(request, self.template_name, context)


class MyTextsView(MaterialListView):
    model = 'text'
    template_name = 'exercises/list_text.html'


class MyTopicsView(MaterialListView):
    model = 'topic'
    template_name = 'exercises/list_topic.html'


class MyExercisesView(MaterialListView):
    model = 'exercise'
    template_name = 'exercises/list_exercise.html'


def one_random_word(request):
    word = Word.objects.order_by('?').first()
    return render(request, 'exercises/check_answer.html', {'word': word})

def check_answer(request):
    is_correct = None
    if request.method == 'POST':
        user_answer = request.POST.get('user_answer')
        word_id = request.POST.get('word_id')
        word = Word.objects.get(id=word_id)
        correct_translation = word.word_rus.split(', ')
        is_correct = user_answer.lower() in correct_translation
        if is_correct:
            return render(request, 'exercises/result.html', {'is_correct': is_correct})
        else:
            return render(request, 'exercises/result.html', {'correct_answer': word.word_rus, 'is_correct': is_correct})
    return render(request, 'exercises/result.html')

def ten_random_words(request):
    words = Word.objects.filter().order_by('?')[:10]
    context = {
        'object_list': words
    }
    return render(request, 'exercises/word_list.html', context)

def game(request):
    words = Word.objects.filter().order_by('?')[:5]
    eng_words = [(word.pk, word.word_eng) for word in words]
    rus_words = [(word.pk, word.word_rus) for word in words]
    eng_list = random.sample(eng_words, 5)
    rus_list = random.sample(rus_words, 5)
    return render(request, 'exercises/game.html', {'eng_list': eng_list, 'rus_list': rus_list})