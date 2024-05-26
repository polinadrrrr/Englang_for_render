from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from accounts.models import Profile
from .models import Quiz, Question, Answer, Choice, Result
from .forms import QuizForm, QuestionForm
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from exercises.views import BookmarkObjectMixin, MaterialListView, UserMaterialListView, UserBookmarksMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Avg
from django.contrib.auth.models import User


# Create your views here.
method_decorator(login_required, name='dispatch')
class QuizListView(ListView):
    model = Quiz
    context_object_name = 'content'
    template_name = 'quizzes/quizzes.html'

    def get_queryset(self):
        return Quiz.objects.filter(question__isnull=False).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_has_result'] = self.request.user.result_set.all()
        context['user'] = self.request.user
        return context


@login_required
def display_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.question_set.first()
    if question:
        return redirect(reverse('display_question', kwargs={'quiz_id': quiz_id, 'question_id': question.pk}))

@login_required
def display_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()
    current_question, next_question = None, None
    for ind, q in enumerate(questions):
        if q.pk == question_id:
            current_question = q
            if ind != len(questions) - 1:
                next_question = questions[ind + 1]
    context = {
        'quiz': quiz, 
        'question': current_question, 
        'next_question': next_question,
        'user': request.user
    }
    return render(request, 'quizzes/display.html', context)

@login_required
def check_answer(request, quiz_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    completed = question.already_completed(request.user)
    is_correct = None
    try:
        if completed:
            return render(request, 'quizzes/partial.html', {
                'question': question,
                'error_message': 'Вы уже отвечали на этот вопрос.'
            })
        if question.type == 'single':
            correct_answer = question.get_answers()
            user_answer = question.answer_set.get(pk=request.POST['answer'])
            choice = Choice(user=request.user, question=question, answer=user_answer)
            choice.save()
            is_correct = correct_answer == user_answer
            result, created = Result.objects.get_or_create(user=request.user, quiz=quiz)
            if is_correct is True:
                result.correct_answers = F('correct_answers') + 1
            else:
                result.wrong_answers = F('wrong_answers') + 1
            result.save()
        elif question.type == 'multiple':
            correct_answer = question.get_answers()
            answers_ids = request.POST.getlist('answer')
            user_answers = []
            if answers_ids:
                for answer_id in answers_ids:
                    user_answer = Answer.objects.get(pk=answer_id)
                    user_answers.append(user_answer.name)
                    choice = Choice(user=request.user, question=question, answer=user_answer)
                    choice.save()
                is_correct = correct_answer == user_answers 
                result, created = Result.objects.get_or_create(user=request.user, quiz=quiz)
                if is_correct is True:
                    result.correct_answers = F('correct_answers') + 1
                else:
                    result.wrong_answers = F('wrong_answers') + 1
                result.save()
    except:
        return render(request, 'quizzes/partial.html', {'question': question})
    context = {
        'is_correct': is_correct, 
        'correct_answer': correct_answer, 
        'question': question
    }
    return render(request,'quizzes/partial.html', context)

@login_required
def retry_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.question_set.first()
    quiz_questions = quiz.question_set.all()
    Choice.objects.filter(user=request.user, question__in=quiz_questions).delete()
    Result.objects.filter(user=request.user, quiz=quiz).update(correct_answers=0, wrong_answers=0)
    return redirect('display_question', quiz_id=quiz_id, question_id=question.pk)

@login_required
def quiz_results(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()
    try:
        choices = Choice.objects.filter(user=user, question__in=questions)
        result = Result.objects.get(user=user, quiz=quiz)
        correct_answers = result.correct_answers
        wrong_answers = result.wrong_answers
    except Result.DoesNotExist:
        return redirect("quizzes")
    context = {
        'quiz': quiz,
        'user': user,
        'choices': choices,
        'questions': questions,
        'correct_answers': correct_answers,
        'wrong_answers': wrong_answers,
        'number': len(questions),
        'skipped': len(questions) - (correct_answers + wrong_answers)
    }
    return render(request, 'quizzes/results.html', context)

method_decorator(login_required, name="dispatch")
class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quizzes/quiz_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.question_set.all()
        return context


method_decorator(login_required, name="dispatch")
class CreateQuizView(CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quizzes/quiz_form.html'

    def get_success_url(self):
        return reverse('quiz_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


@login_required
def create_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('quiz_details', quiz_id)
    context = { 'form': form }
    return render(request, 'quizzes/question_form.html', context)

@login_required
def create_answer(request, quiz_id, question_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Статья не найдена")
    question.answer_set.create(name=request.POST['name'], is_correct=request.POST.get('is_correct', False))
    return HttpResponseRedirect(reverse('quiz_details', args=(quiz.id,)))


method_decorator(login_required, name="dispatch")
class UpdateQuizView(UpdateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quizzes/quiz_form.html'
    success_url = reverse_lazy('quizzes')


@login_required
def update_question(request, quiz_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    form = QuestionForm(instance=question)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('quiz_details', quiz_id)
    context = { 'form': form, 'question': question }
    return render(request, 'quizzes/question_form.html', context)


method_decorator(login_required, name="dispatch")
class DeleteQuizView(DeleteView):
    model = Quiz
    template_name = 'delete.html'
    success_url = reverse_lazy('quizzes')


@login_required
def delete_question(request, quiz_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.delete()
        return redirect('quiz_details', quiz_id)
    context = {'object': question}
    return render(request, 'delete.html', context)

@login_required
def delete_answer(request, quiz_id, answer_id):
    quiz = Quiz.objects.get(id=quiz_id)
    answer = Answer.objects.get(id=answer_id)
    answer.delete()
    return HttpResponseRedirect(reverse('quiz_details', args=(quiz.id,)))


class UserQuizzesView(UserMaterialListView):
    model = Quiz
    template_name = 'quizzes/quizzes.html'

    def get_queryset(self):
        return Quiz.objects.filter(question__isnull=False).distinct()


class MyQuizzesView(MaterialListView):
    model = 'quiz'
    template_name = 'quizzes/quizzes.html'
