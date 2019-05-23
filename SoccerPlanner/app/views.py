"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from app.forms import *

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

def accountcreatesuccessful(request):
    """Renders the successful account creation page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/accountcreatesuccessful.html'
    )


""" NitroBolon """
def matchcreate(request):
    """View for creating matches"""
    if request.method == 'POST':
        match_form = MatchCreateForm(request.POST)
        if match_form.is_valid():
            match_form.save()
            return redirect('manage')
    else:
        match_form = MatchCreateForm()

    return render(
        request,
        'app/matchcreate.html',
        {
            'title': 'Match Creator',
            'match_form': match_form,
        }
    )

def playercreate(request):
    """View for creating players"""
    if request.method == 'POST':
        player_form = PlayerCreateForm(request.POST)
        if player_form.is_valid():
            player_form.save()
            return redirect('manage')
    else:
        player_form = PlayerCreateForm()

    return render(
        request,
        'app/playercreate.html',
        {
            'title': 'Player Creator',
            'player_form': player_form,
        }
    )

def matchedit(request):
        """View for editing matches"""
        if request.method == 'POST':
            matchedit_form = MatchEditForm(request.POST)
            if matchedit_form.is_valid():
                #opt = matchedit_form.cleaned_data['listOfMatches']
                a=Match.objects.get(name = opt.name, listOfMatches = opt.listOfMatches)
                matchedit_form = MatchEditForm(request.POST, instance = a)
                matchedit_form.save()
                return redirect('manage')
        else:
            matchedit_form = MatchEditForm()
            return render(request, 'app/matchedit.html', {'matchedit_form': matchedit_form})

def playeredit(request):
        """View for editing players"""
        if request.method == 'POST':
            playeredit_form = PlayerEditForm(request.POST)
            if playeredit_form.is_valid():
                opt = playeredit_form.cleaned_data['listOfPlayers']
                a=Player.objects.get(name = opt.name,secondName = opt.secondName)
                playeredit_form = PlayerEditForm(request.POST, instance = a)
                a.save()
                return redirect('manage')
        else:
            playeredit_form = PlayerEditForm()
            return render(request, 'app/playeredit.html', {'playeredit_form': playeredit_form})

def matchdelete(request):
    if request.method == 'POST':
            matchdelete_form = MatchDeleteForm(request.POST)
            if matchdelete_form.is_valid():
                opt = matchdelete_form.cleaned_data['listOfMatches']
                a=Match.objects.get(team1 = opt.team1,team2 = opt.team2)
                matchdelete_form = MatchDeleteForm(request.POST, instance = a)
                a.delete()
                return redirect('manage')
    else:
        matchdelete_form = MatchDeleteForm()
    return render(request, 'app/matchdelete.html', {'matchdelete_form': matchdelete_form})

def playerdelete(request):
    if request.method == 'POST':
            playerdelete_form = PlayerDeleteForm(request.POST)
            if playerdelete_form.is_valid():
                opt = playerdelete_form.cleaned_data['listOfPlayers']
                a=Player.objects.get(name = opt.name,secondName = opt.secondName)
                playerdelete_form = PlayerDeleteForm(request.POST, instance = a)
                a.delete()
                return redirect('manage')
    else:
        playerdelete_form = PlayerDeleteForm()
    return render(request, 'app/playerdelete.html', {'playerdelete_form': playerdelete_form})