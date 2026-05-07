from django.urls import path
from . import views


urlpatterns = [
    path('', views.QuizListView.as_view(), name='quizzes'),
    path('<int:quiz_id>/', views.display_quiz, name='display_quiz'),
    path('<int:quiz_id>/questions/<int:question_id>', views.display_question, name='display_question'),
    path('<int:quiz_id>/questions/<int:question_id>/grade/', views.check_answer, name='check_answer'),
    path('results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),

    path('quiz/create/', views.CreateQuizView.as_view(), name='create_quiz'),
    path('quiz/update/<int:pk>/', views.UpdateQuizView.as_view(), name='update_quiz'),
    path('quiz/<int:pk>/delete/', views.DeleteQuizView.as_view(), name='delete_quiz'),

    path('quiz/<int:pk>/detail/', views.QuizDetailView.as_view(), name='quiz_details'),

    path('quiz/<int:quiz_id>/question/create/', views.create_question, name='create_question'),
    path('quiz/<int:quiz_id>/question/update/<int:question_id>/', views.update_question, name='update_question'),
    
    path('quiz/<int:quiz_id>/question/delete/<int:question_id>/', views.delete_question, name='delete_question'),

    path('quiz/<int:quiz_id>/question/<int:question_id>/answer/create/', views.create_answer, name='create_answer'),
    path('quiz/<int:quiz_id>/answer/<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),

    path('quiz/<int:quiz_id>/retry/', views.retry_quiz, name='retry_quiz'),

    path('user_quizzes/<str:username>/', views.UserQuizzesView.as_view(), name='user_quizzes'), 
    path('my_quizzes/', views.MyQuizzesView.as_view(), name='my_quizzes'), 
]
