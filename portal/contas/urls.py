from cgitb import html
from django.urls import path
from django.contrib.auth import views as auth_views
from contas.views import UserLoginView, UserCreateView, UserUpdateView, Timeout
from . import admin as admin_views

urlpatterns = [
    path('login/',UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),   
    path('novo-usuario/', UserCreateView.as_view(), name='user_new'),
      
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_change'), 
    
	
      
    path('password_change/', auth_views.PasswordChangeView.as_view(form_class=admin_views.UserPasswordChangeForm,template_name='reset/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='reset/password_change_done.html'), name='password_change_done'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=admin_views.UserPasswordResetForm, template_name='reset/password_reset_form.html'), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=admin_views.UserPasswordResetConfirmForm, template_name='reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='reset/password_reset_complete.html'), name='password_reset_complete'),

    path('timeout/', Timeout.as_view(), name='timeout'),
]
