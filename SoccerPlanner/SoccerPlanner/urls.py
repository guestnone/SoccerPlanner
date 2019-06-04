"""
Definition of urls for SoccerPlanner.
"""

from datetime import datetime
from django.urls import path, re_path, include
from django.contrib import admin
from django.contrib.auth.views import *
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    ## path('index/', views.home, name='index'),
    ##path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('manage/', views.manage, name='manage'),
    path('calendar/', views.calendarview.as_view(), name='calendar'),
    path('account/', views.account, name='account'),
    path('accountcreate/', views.accountcreate, name='accountcreate'),
    path('accountcreatesuccessful/', views.accountcreatesuccessful, name='accountcreatesuccessful'),
    path('teamcreate/', views.teamcreate, name='teamcreate'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/(<event_id>\d+)/', views.event, name='event_edit'),
    path('stagecreate/', views.stagecreate, name='stagecreate'),
    path('stagecreatesuccessful/',views.stagecreatesuccessful, name = 'stagecreatesuccessful'),
    path('tournamentcreate', views.tournamentcreate, name='tournamentcreate'),
    path('stagedeletesuccessful',views.stagedeletesuccessful, name = 'stagedeletesuccessful'),
    path('captcha', views.captcha,name='captcha'),
    path('stageeditsuccessful',views.stageeditsuccessful, name='stageeditsuccessful'),
    path('account/passwordreset/', PasswordResetView.as_view(template_name='app/passwordreset.html'), name='passwordreset'),
    path('account/passwordresetdone/', PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='app/passwordresetconfirm.html'), name='password_reset_confirm'),
    path('account/resetlogged/', PasswordChangeView.as_view(template_name='app/passwordresetconfirmlogged.html'), name='password_reset_confirm_logged'),
    path('account/resetloggeddone/', PasswordChangeDoneView.as_view(template_name='app/passwordresetloggeddone.html'), name='password_change_done'),
    path('account/reset/done/', PasswordResetCompleteView.as_view(template_name='app/passwordresetcomplete.html'), name='password_reset_complete'),
]
