"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from app.forms import *
from .models import *
from django import forms
from django.views import generic
from django.utils.safestring import mark_safe


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


def manage(request):
    """ All-encompassing view for management stuff """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/manage.html',
        {
            'title': 'Dashboard',
        }
    )


def account(request):
    """ View for account management """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/account.html',
        {
            'title': 'Account',
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
                'title': 'Calendar (editable)',
            }
        )
    else:
        return render(
            request,
            'app/calendar.html',
            {
                'title': 'Calendar',
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


def accountcreatesuccessful(request):
    """Renders the successful account creation page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/accountcreatesuccessful.html'
    )


"""View for creating teams"""


def teamcreate(request):
    if request.method == 'POST':
        team_squad_form = TeamSquadForm(request.POST)
        team_form = TeamForm(request.POST)
        team_squad_edit_form = TeamSquadEditForm(request.POST)
        team_edit_form = TeamEditForm(request.POST)
        if team_squad_form.is_valid():
            if team_squad_edit_form.is_valid():
                opt = team_squad_edit_form.cleaned_data['listOfSquads']
                a = TeamSquad.objects.get(name=opt.name, playerID=opt.playerID)
                team_squad_edit_form = TeamSquadEditForm(request.POST, instance=a)
                team_squad_edit_form.save()
                return redirect('teamcreate')
            team_squad_form.save()
        elif team_form.is_valid():
            if team_edit_form.is_valid():
                opt = team_edit_form.cleaned_data['listOfTeams']
                a = Team.objects.get(name=opt.name, country=opt.country, squad=opt.squad)
                team_edit_form = TeamEditForm(request.POST, instance=a)
                team_edit_form.save()
                return redirect('teamcreate')
            team_form.save()
        return redirect('teamcreate')
    else:
        team_squad_form = TeamSquadForm()
        team_form = TeamForm()
        team_squad_edit_form = TeamSquadEditForm()
        team_edit_form = TeamEditForm()

    return render(
        request,
        'app/teamcreate.html',
        {
            'title': 'Team Creator',
            'team_squad_form': team_squad_form,
            'team_form': team_form,
            'team_squad_edit_form': team_squad_edit_form,
            'team_edit_form': team_edit_form,
        }
    )
