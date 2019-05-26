"""
Definition of views.
"""

from datetime import *
from calendar import monthrange, calendar
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from app.forms import *
from .models import *
from django.contrib import messages
from django import forms
from django.contrib import messages
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar

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

#def calendar(request):
#    """ View for displaying calendar """
#    assert isinstance(request, HttpRequest)
#    if request.user.is_authenticated:
#        return render(
#            request,
#            'app/calendar.html',
#            {
#               'title':'Calendar (editable)',
#            }
#        )
#    else:
#        return render(
#            request,
#            'app/calendar.html',
#            {
#                'title':'Calendar',
#            }
#        )

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
  

def stagedelete(request):
    if request.method == 'POST':
            form = StageDeleteForm(request.POST)
            if form.is_valid():
                opt = form.cleaned_data['listOfStages']
                a=Stage.objects.get(name = opt.name, listOfMatches = opt.listOfMatches)
                form = StageDeleteForm(request.POST, instance = a)
                a.delete()
                #form.delete()
                return redirect('stagedeletesuccessful')
    else:
        form = StageDeleteForm()
    return render(request, 'app/stagedelete.html', {'form': form})
def stagedeletesuccessful(request):
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'app/stagedeletesuccessful.html'
    )
class calendarview(generic.ListView):
    model = Event
    template_name = 'app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, self.request)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'app/event.html', {'form': form})
def captcha(request):
    if request.POST:
        form= CaptchaForm(request.POST)
        if form.is_valid():
            human = True
            return redirect("/")
    else:
        form = CaptchaForm()
    return render(request,'app/captcha.html', {'form' : form})
