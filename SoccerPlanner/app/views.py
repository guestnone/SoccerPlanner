"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import *
from app.forms import *
from django.contrib import messages
from django import forms
from django.views import generic
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def manage(request):
    """ All-encompassing view for management stuff """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/manage.html',
        {
            'title':'Dashboard',
        }
    )

def account(request):
    """ View for account management """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/account.html',
        {
            'title':'Account',
        }
    )

def calendar(request):
    """ View for displaying calendar """
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return render(
            request,
            'app/calendar.html',
            {
                'title':'Calendar (editable)',
            }
        )
    else:
        return render(
            request,
            'app/calendar.html',
            {
                'title':'Calendar',
            }
        )

def accountcreate(request):
    """ View for creating user accounts """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accountcreatesuccessful')
    else:
        form = SignUpForm()
    return render(request, 'app/accountcreate.html', {'form': form})

def stagecreate(request):     
        if request.method == 'POST':
            form = StageForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('stagecreatesuccessful')
        else:
            form = StageForm()
        return render(request, 'app/stagecreate.html', {'form': form})


def stageedit(request):
        if request.method == 'POST':
            form = StageEditForm(request.POST)
            if form.is_valid():
                opt = form.cleaned_data['listOfStages']
                a=Stage.objects.get(name = opt.name, listOfMatches = opt.listOfMatches)
                form = StageEditForm(request.POST, instance = a)
                form.save()
                return redirect('stageeditsuccessful')
        else:
            form = StageEditForm()
        return render(request, 'app/stageedit.html', {'form': form})
        
def accountcreatesuccessful(request):
    """Renders the successful account creation page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/accountcreatesuccessful.html'
    )
def stagecreatesuccessful(request):
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'app/stagecreatesuccessful.html'
    )
def stageeditsuccessful(request):
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'app/stageeditsuccessful.html'
    )

