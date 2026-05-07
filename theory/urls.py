from django.contrib import admin
from django.urls import path
from . import views
from .models import Lesson, Textbook
from exercises.models import Text, Topic, Exercise

urlpatterns = [
    path('themes/', views.ThemeListView.as_view(), name='theme_list'),
    path('theme/<slug:theme_slug>/', views.theme_detail, name='theme'),
    path('theme/<slug:theme_slug>/<str:content_type>/', views.theme_content, name='theme_content'),

    path('create_theme/', views.CreateThemeView.as_view(), name='create_theme'),
    path('update_theme/<slug:slug>/', views.UpdateThemeView.as_view(), name='update_theme'),
    path('delete_theme/<slug:slug>/', views.DeleteThemeView.as_view(), name='delete_theme'),
    
    path('create_lesson/', views.create_lesson, name='create_lesson'),
    path('update_lesson/<str:lesson_slug>/', views.update_lesson, name='update_lesson'),
    path('delete_lesson/<slug:slug>/', views.DeleteLessonView.as_view(), name='delete_lesson'),

    path('lesson/<str:theme_slug>/<str:lesson_slug>/comment/', views.comments, name='comments'),
    
    path('lesson/<str:theme_slug>/<str:lesson_slug>/', views.lesson, name='lesson'),
    path('materials/', views.materials, name='materials'),
    path('bookmark_lesson/<int:lesson_id>/', views.BookmarkLessonView.as_view(), name='bookmark_lesson'),
        
    path('lesson_bookmarks/', views.UserLessonsBookmarksView.as_view(), name='user_lesson_bookmarks'), #
    path('textbooks_bookmarks/', views.UserTextbooksBookmarksView.as_view(), name='user_textbooks_bookmarks'),

    path('user_lessons/<str:username>/', views.UserLessonsView.as_view(), name='user_lessons'),
    path('my_lessons/', views.MyLessonsView.as_view(), name='my_lessons'),
    
    path('create_textbook/', views.create_textbook, name='create_textbook'),
    path('update_textbook/<str:textbook_slug>/', views.update_textbook, name='update_textbook'),
    path('delete_textbook/<slug:slug>/', views.DeleteTextbookView.as_view(), name='delete_textbook'),

    path('textbook/<slug:slug>/', views.TextbookDetailView.as_view(), name='textbook_detail'),
    
    path('bookmark_textbook/<int:textbook_id>/', views.BookmarkTextbookView.as_view(), name='bookmark_textbook'),
    
    path('lessons/tag/<slug:tag_slug>/', views.LessonsByTagView.as_view(), name='lessons_by_tag'),
    path('textbooks/tag/<slug:tag_slug>/', views.TextbooksByTagView.as_view(), name='textbooks_by_tag'),

    path('lessons/', views.LessonListView.as_view(), name='lessons'),
    path('textbooks/', views.TextbookListView.as_view(), name='textbooks'),
    path('texts/', views.TextListView.as_view(), name='texts'),
    path('topics/', views.TopicListView.as_view(), name='topics'),
    path('exercises/', views.ExerciseListView.as_view(), name='exercises'),
]
