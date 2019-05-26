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


def matchcreate(request):
    """View for creating matches"""
    if request.method == 'POST':
        match_form = MatchCreateForm(request.POST)
        matchedit_form = MatchEditForm(request.POST)
        matchdelete_form = MatchDeleteForm(request.POST)
        shooters_form = ShootersForm(request.POST)
        if match_form.is_valid():
            match_form.save()
            return redirect('matchcreate')
        elif matchedit_form.is_valid():
                opt = matchedit_form.cleaned_data['listOfMatches']
                a=Match.objects.get(team1 = opt.team1, team2 = opt.team2, matchID=opt.matchID)
                matchedit_form = MatchEditForm(request.POST, instance = a)
                matchedit_form.save()
                return redirect('matchcreate')
        elif matchdelete_form.is_valid():
                opt = matchdelete_form.cleaned_data['listOfMatches']
                a=Match.objects.get(team1 = opt.team1, team2 = opt.team2, matchID=opt.matchID)
                matchdelete_form = MatchDeleteForm(request.POST, instance = a)
                a.delete()
                return redirect('matchcreate')
        elif shooters_form.is_valid():
                opt = shooters_form.cleaned_data['listOfShooters']
                a=Player.objects.get(name = opt.name,secondName = opt.secondName, role= opt.role, playerID=opt.playerID)
                shooters_form = ShootersForm(request.POST, instance = a)
                shooters_form.delete()
                return redirect('matchcreate')
    else:
        match_form = MatchCreateForm()
        matchedit_form = MatchEditForm()
        matchdelete_form = MatchDeleteForm()
        shooters_form = ShootersForm()
    return render(
        request,
        'app/matchcreate.html',
        {
            'title': 'Match Manager',
            'match_form': match_form,
            'matchedit_form': matchedit_form,
            'matchdelete_form': matchdelete_form,
            'shooters_form': shooters_form,
        }
    )

def playercreate(request):
    if request.method == 'POST':
        player_form = PlayerCreateForm(request.POST)
        playeredit_form = PlayerEditForm(request.POST)
        playerdelete_form = PlayerDeleteForm(request.POST)
        if playeredit_form.is_valid():
            opt = playeredit_form.cleaned_data['listOfPlayers']
            a=Player.objects.get(name = opt.name,secondName = opt.secondName, role= opt.role, playerID=opt.playerID)
            playeredit_form = PlayerEditForm(request.POST, instance = a)
            playeredit_form.save()
            return redirect('playercreate')
        elif player_form.is_valid():
            player_form.save()
            return redirect('playercreate')
        elif playerdelete_form.is_valid():
            opt = playerdelete_form.cleaned_data['listOfPlayers']
            a=Player.objects.get(name = opt.name,secondName = opt.secondName, role= opt.role, playerID=opt.playerID)
            playerdelete_form = PlayerDeleteForm(request.POST, instance = a)
            a.delete()
            return redirect('playercreate')
    else:
        player_form = PlayerCreateForm()
        playeredit_form = PlayerEditForm()
        playerdelete_form = PlayerDeleteForm()

    return render(
        request, 'app/playercreate.html',
        {'title': 'Player Manager',
        'player_form': player_form,
        'playeredit_form': playeredit_form,
        'playerdelete_form': playerdelete_form,}
        )


