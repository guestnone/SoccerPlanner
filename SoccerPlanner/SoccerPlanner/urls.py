"""
Definition of urls for SoccerPlanner.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
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
    path('calendar/', views.calendar, name='calendar'),
    path('account/', views.account, name='account'),
    path('accountcreate/', views.accountcreate, name='accountcreate'),
    path('accountcreatesuccessful/', views.accountcreatesuccessful, name='accountcreatesuccessful'),
    path('stagecreate/', views.stagecreate, name='stagecreate'),
    path('stagecreatesuccessful/',views.stagecreatesuccessful, name = 'stagecreatesuccessful'),
    path('stageedit/',views.stageedit, name = 'stageedit'),
    path('stageeditsuccessful',views.stageeditsuccessful, name='stageeditsuccessful'),
]
