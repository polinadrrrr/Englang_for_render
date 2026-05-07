# accounts/ login/ [name='login']
# accounts/ logout/ [name='logout']
# accounts/ password_change/ [name='password_change']
# accounts/ password_change/done/ [name='password_change_done']
# accounts/ password_reset/ [name='password_reset']
# accounts/ password_reset/done/ [name='password_reset_done']
# accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/ reset/done/ [name='password_reset_complete']

from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    
    path('password-reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html',
        success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    
    path('profile/', views.user_profile_detail, name='profile'),
    path('profile/edit/', views.update_profile, name='profile_edit'),
    path('profile/<str:username>/', views.user_profile_detail, name='user_profile_detail'),
    path('profiles/', views.profiles, name='profiles'),
        
    path('add_goal/', views.AddGoalView.as_view(), name='add_goal'),
    path('update_goal/<str:goal_slug>/', views.UpdateGoalView.as_view(), name='update_goal'),
    path('delete_goal/<str:goal_slug>/', views.DeleteGoalView.as_view(), name='delete_goal'),
    
    path('follow_unfollow/<str:username>/', views.FollowUnfollowView.as_view(), name='follow_unfollow'),
    #path('new_published_lessons/', views.new_published_lessons, name='new_published_lessons'),
]