from django.urls import re_path, path
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from . import views
# from ckeditor_uploader import views as editor_views

urlpatterns = [
    path('password_reset/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('<slug>/follow/', views.user_follow_toggle, name='user_follow_toggle'),
    path('login/', views.login, name='login'),
    path('logout/<slug>/', views.logout_member, name='logout_page'),
    path('update/myusername/',  views.update_username, name='update_username'),
    re_path(r'^(?P<slug>[\w.-]+)/dashboard/', views.dashboard, name='dashboard'),
    path('social/<slug>/update/', views.update_social_account, name='update_social_account'),
    path('<slug>/update/', views.update_user, name='update_user'),
    re_path(r'^(?P<slug>[\w.-]+)/comment_hover_user/', views.comments_hover_user, name='comment_hover_user')
    ]
