from django.urls import path
from . import views


urlpatterns = [
    path('text/<slug:slug>/', views.TextDetail.as_view(), name='text_details'),
    path('topic/<str:topic_slug>/', views.topic_details, name='topic_details'),
    path('exercise/<slug:slug>/', views.ExerciseDetail.as_view(), name='exercise_details'),

    path('create_text/', views.CreateTextView.as_view(), name='create_text'),
    path('create_word/', views.CreateWordView.as_view(), name='create_word'),
    path('create_topic/', views.CreateTopicView.as_view(), name='create_topic'),
    path('create_exercise/', views.CreateExerciseView.as_view(), name='create_exercise'),

    path('update_text/<slug:slug>/', views.UpdateTextView.as_view(), name='update_text'),
    path('update_word/<int:pk>/', views.UpdateWordView.as_view(), name='update_word'),
    path('update_topic/<slug:slug>/', views.UpdateTopicView.as_view(), name='update_topic'),
    path('update_exercise/<slug:slug>/', views.UpdateExerciseView.as_view(), name='update_exercise'),
    
    path('delete_text/<slug:slug>/', views.DeleteTextView.as_view(), name='delete_text'),
    path('delete_word/<int:pk>/', views.DeleteWordView.as_view(), name='delete_word'),
    path('delete_topic/<slug:slug>/', views.DeleteTopicView.as_view(), name='delete_topic'),
    path('delete_exercise/<slug:slug>/', views.DeleteExerciseView.as_view(), name='delete_exercise'),
    
    path('topic/<str:topic_slug>/add_word/<int:word_id>/', views.add_word_to_topic, name='add_word_to_topic'),
    path('topic/<str:topic_slug>/remove_word/<int:word_id>/', views.remove_word_from_topic, name='remove_word_from_topic'),
    
    path('bookmark_text/<int:text_id>/', views.BookmarkTextView.as_view(), name='bookmark_text'),
    path('bookmark_topic/<int:topic_id>/', views.BookmarkTopicView.as_view(), name='bookmark_topic'),

    path('ten_random_words_from_bookmarks/', views.ten_random_words_from_bookmarks, name='ten_random_words_from_bookmarks'),
    
    path('texts_bookmarks/', views.UserTextsBookmarksView.as_view(), name='user_texts_bookmarks'),
    path('topics_bookmarks/', views.UserTopicsBookmarksView.as_view(), name='user_topics_bookmarks'),
    
    path('user_texts/<str:username>/', views.UserTextsView.as_view(), name='user_texts'),
    path('user_topics/<str:username>/', views.UserTopicsView.as_view(), name='user_topics'),
    path('user_exercises/<str:username>/', views.UserExercisesView.as_view(), name='user_exercises'),

    path('my_texts/', views.MyTextsView.as_view(), name='my_texts'),
    path('my_topics/', views.MyTopicsView.as_view(), name='my_topics'),
    path('my_exercises/', views.MyExercisesView.as_view(), name='my_exercises'),

    path('one_word/', views.one_random_word, name='one_word'),
    path('one_word/check_answer/', views.check_answer, name='check_answer'),
    path('ten_random_words/', views.ten_random_words, name='ten_random_words'),

    path('game/', views.game, name='game'),
]