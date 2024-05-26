from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from exercises.models import Text, Topic, Exercise
from exercises.views import BookmarkObjectMixin, MaterialListView, UserMaterialListView, UserBookmarksMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Theme, Lesson, Comment, Tag, Textbook
from .forms import LessonForm, CommentForm, TextbookForm, ThemeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import Profile
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Create your views here.
@method_decorator(login_required, name="dispatch")
class CreateThemeView(CreateView):
    model = Theme
    form_class = ThemeForm
    template_name = 'theory/theme_form.html'
    success_url = reverse_lazy('theme_list')


@login_required
def create_lesson(request):
    author = Profile.get_profile(request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.author = author
            lesson.save()
            tags = make_tags(request.POST.get('newtags', '').split())
            lesson.tags.add(*tags)
            return redirect('index')
    else:
        form = LessonForm()
    return render(request, 'theory/lesson_form.html', {'form': form})

def make_tags(newtags):
    tags = []
    for tag_name in newtags:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        tags.append(tag)
    return tags

@login_required
def create_textbook(request):
    if request.method == 'POST':
        form = TextbookForm(request.POST, request.FILES)
        if form.is_valid():
            textbook = form.save()
            newtags = request.POST.get('newtags', '').replace(',', ' ').split()
            tags = make_tags(newtags)
            textbook.tags.add(*tags)
            return redirect(reverse('materials'))
        else:
            messages.error(request, 'Форма заполнена неверно')
    else:
        form = TextbookForm()
    context = {
        "form": form,
    }
    return render(request, 'theory/textbook_form.html', context)


@method_decorator(login_required, name="dispatch")
class UpdateThemeView(UpdateView):
    model = Theme
    form_class = ThemeForm
    template_name = 'theory/theme_form.html'
    success_url = reverse_lazy('theme_list')


@login_required
def update_lesson(request, lesson_slug):
    profile = Profile.get_profile(request.user)
    lesson = get_object_or_404(Lesson, slug=lesson_slug, author=profile)    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            lesson = form.save()
            newtags = request.POST.get('newtags', '').replace(',', ' ').split()
            tags = make_tags(newtags)
            lesson.tags.set(tags)
            return redirect(reverse("materials"))
        else:
            messages.error(request, 'Форма заполнена неверно')
    else:
        form = LessonForm(instance=lesson)    
    return render(request, 'theory/lesson_form.html', {'form': form, 'lesson': lesson})

@login_required
def update_textbook(request, textbook_slug):
    textbook = get_object_or_404(Textbook, slug=textbook_slug)    
    if request.method == 'POST':
        form = TextbookForm(request.POST, request.FILES, instance=textbook)
        if form.is_valid():
            textbook = form.save()
            newtags = request.POST.get('newtags', '').replace(',', ' ').split()
            tags = make_tags(newtags)
            textbook.tags.set(tags)
            messages.success(request, 'Textbook updated successfully.')
            return redirect(reverse("materials"))
        else:
            messages.error(request, 'There was an error updating the textbook.')
    else:
        form = TextbookForm(instance=textbook)    
    context = {
        'form': form,
        'textbook': textbook
    }
    return render(request, 'theory/textbook_form.html', context)


@method_decorator(login_required, name="dispatch")
class DeleteThemeView(DeleteView):
    model = Theme
    template_name = 'delete.html'
    success_url = reverse_lazy('theme_list')


@method_decorator(login_required, name="dispatch")
class DeleteLessonView(DeleteView):
    model = Lesson
    template_name = 'delete.html'
    success_url = reverse_lazy('theme_list')


@method_decorator(login_required, name="dispatch")
class DeleteTextbookView(DeleteView):
    model = Textbook
    template_name = 'delete.html'
    success_url = reverse_lazy('theme_list')


class ThemeListView(ListView):
    model = Theme
    template_name = 'theory/theme_list.html'


def get_tags(lessons):
    tags = set()
    for lesson in lessons:
        for tag in lesson.tags.all():
            tags.add(tag)
    return tags

def theme_detail(request, theme_slug):
    theme = get_object_or_404(Theme, slug=theme_slug)
    content_types = {
        'lesson': Lesson.objects.filter(theme=theme, published=True),
        'textbook': Textbook.objects.filter(theme=theme),
        'text': Text.objects.filter(theme=theme),
        'topic': Topic.objects.filter(theme=theme),
        'exercise': Exercise.objects.filter(theme=theme),
    }
    context = {
        'theme': theme,
        'content_types': content_types,
    }
    return render(request, 'theory/theme.html', context)

def theme_content(request, theme_slug, content_type):
    theme = get_object_or_404(Theme, slug=theme_slug)
    content_models = {
        'lesson': Lesson,
        'textbook': Textbook,
        'text': Text,
        'topic': Topic,
        'exercise': Exercise,
    }
    model = content_models.get(content_type)
    if model is None:
        raise Http404("Content type does not exist")
    content = model.objects.filter(theme=theme)
    context = {
        'theme': theme,
        'content_type': content_type,
        'content': content,
    }
    if content_type == 'lesson' or content_type == 'textbook':
        return render(request, f'theory/list_{content_type}.html', context)
    else:
        return render(request, f'exercises/list_{content_type}.html', context)

def materials(request):
    query = request.GET.get('q', '')
    theme = Theme.objects.filter(name__icontains=query)
    tag = Tag.objects.filter(name__icontains=query)
    common_filters = (
        Q(name__icontains=query) |
        Q(slug__icontains=query) |
        Q(theme__in=theme)
    )
    theory_filters = (
        Q(tags__in=tag) |
        Q(description__icontains=query)
    )
    author_filters = (
        Q(author__user__username__icontains=query) |
        Q(author__user__first_name__icontains=query) |
        Q(author__user__last_name__icontains=query)
    )
    lessons = Lesson.objects.filter(published=True).filter(common_filters | theory_filters | author_filters | Q(content__icontains=query)).distinct()
    textbooks = Textbook.objects.filter(common_filters | theory_filters | Q(author__icontains=query)).distinct()
    texts = Text.objects.filter(common_filters | author_filters | author_filters).distinct()
    topics = Topic.objects.filter(common_filters | author_filters).distinct()
    exercises = Exercise.objects.filter(common_filters | author_filters).distinct()
    context = {
        'lessons': lessons,
        'textbooks': textbooks,
        'texts': texts,
        'topics': topics,
        'exercises': exercises,
    }
    return render(request, 'theory/materials.html', context)

def lesson(request, theme_slug, lesson_slug):
    lesson = get_object_or_404(Lesson, theme__slug=theme_slug, slug=lesson_slug)
    tags = get_tags([lesson])
    comments = Comment.objects.filter(lesson=lesson).order_by('created_at')
    context = {
        'lesson': lesson,
        'comments': comments,
        'tags': tags
    }
    return render(request, 'theory/lesson.html', context)

@login_required
def comments(request, theme_slug, lesson_slug):
    lesson = Lesson.objects.get(theme__slug=theme_slug, slug=lesson_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent')
            comment = form.save(commit=False)
            comment.author = Profile.get_profile(request.user)
            comment.lesson = lesson
            if parent_id:
                comment.parent_id = parent_id
            comment.save()
        return redirect('lesson', theme_slug=theme_slug, lesson_slug=lesson_slug)


@method_decorator(login_required, name="dispatch")
class BookmarkLessonView(BookmarkObjectMixin, View):
    def get_object(self):
        return get_object_or_404(Lesson, id=self.kwargs.get('lesson_id'))


class UserLessonsView(UserMaterialListView):
    model = Lesson
    template_name = 'theory/list_lesson.html'


class MyLessonsView(MaterialListView):
    model = 'lesson'
    template_name = 'theory/list_lesson.html'


@method_decorator(login_required, name="dispatch")
class BookmarkTextbookView(BookmarkObjectMixin, View):
    def get_object(self):
        return get_object_or_404(Textbook, id=self.kwargs.get('textbook_id'))


class ContentByTagMixin:
    model = None
    template_name = 'theory/materials.html'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        return self.model.objects.filter(tags__in=[tag])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        tags = get_tags(queryset)
        context.update({
            self.model.__name__.lower() + 's': queryset,
            'tags': tags
        })
        return context


class LessonsByTagView(ContentByTagMixin, ListView):
    model = Lesson

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)


class TextbooksByTagView(ContentByTagMixin, ListView):
    model = Textbook


class TextbookDetailView(DetailView):
    model = Textbook
    template_name = 'theory/textbook_detail.html'
    context_object_name = 'textbook'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = get_tags([context['textbook']])
        return context


class UserLessonsBookmarksView(LoginRequiredMixin, UserBookmarksMixin):
    model = Lesson
    context_object_name = 'lessons'


class UserTextbooksBookmarksView(LoginRequiredMixin, UserBookmarksMixin):
    model = Textbook
    context_object_name = 'textbooks'


class LessonListView(ListView):
    model = Lesson
    template_name = 'theory/materials.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class TextbookListView(ListView):
    model = Textbook
    template_name = 'theory/materials.html'
    context_object_name = 'textbooks'


class TextListView(ListView):
    model = Text
    template_name = 'theory/materials.html'
    context_object_name = 'texts'


class TopicListView(ListView):
    model = Topic
    template_name = 'theory/materials.html'
    context_object_name = 'topics'


class ExerciseListView(ListView):
    model = Exercise
    template_name = 'theory/materials.html'
    context_object_name = 'exercises'
