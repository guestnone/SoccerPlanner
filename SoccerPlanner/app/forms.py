"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm, DateInput, TextInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from app.models import Player, TeamSquad, Team, Stage, Match, Event, Tournament, ShootersMatch
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput({'class': 'form-control', 'placeholder': 'Password'}))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
          'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
          'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class StageForm(ModelForm):
    name = forms.CharField(max_length = 20,required = True)
    listOfMatches = forms.ModelChoiceField(queryset = Match.objects.all(),required = False, label = "Match ",empty_label = None)
    class Meta:
        model = Stage
        listOfMatches = [Match]
        fields = ('name','listOfMatches')

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name + " "+ obj.listOfMatches.team1.name + " " + obj.listOfMatches.team2.name


class StageEditForm(ModelForm):
    listOfStages = MyModelChoiceField(queryset = Stage.objects.all(), label = "Stage ", required = True, empty_label= None)
    listOfMatches = forms.ModelChoiceField(queryset = Match.objects.all(),required = True, label = "Match ",empty_label = None)
    class Meta:
        model = Stage
        fields = ('listOfStages','name','listOfMatches')

class TeamSquadForm(ModelForm):
    name = forms.CharField(max_length=20, required=True, help_text='Required.')
    playerID = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), widget=forms.CheckboxSelectMultiple, label="Player ", required=True)

    class Meta:
        model = TeamSquad
        fields = ('name', 'playerID', )


class TeamForm(ModelForm):
    name = forms.CharField(max_length=20, required=True, help_text='Required.')
    country = forms.CharField(max_length=20, required=True, help_text='Required.')
    squad = forms.ModelChoiceField(queryset=TeamSquad.objects.all(), required=True, empty_label="(Nothing)")

    class Meta:
        model = Team
        fields = ('name', 'country', 'squad', )


class TeamSquadEditForm(ModelForm):
    listOfSquads = forms.ModelChoiceField(queryset=TeamSquad.objects.all(), label="Squad ", required=True, empty_label="(Nothing)")
    playerID = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), widget=forms.CheckboxSelectMultiple, label="Player ", required=True)
    class Meta:
        model = TeamSquad
        fields = ('listOfSquads', 'name', 'playerID', )


class TeamEditForm(ModelForm):
    listOfTeams = forms.ModelChoiceField(queryset=Team.objects.all(), label="Team ", required=True, empty_label="(Nothing)")
    squad = forms.ModelChoiceField(queryset=TeamSquad.objects.all(), required=True, empty_label="(Nothing)")

    class Meta:
        model = Team
        fields = ('listOfTeams', 'name', 'country', 'squad', )

class TeamSquadDeleteForm(ModelForm):
    listOfSquads = forms.ModelChoiceField(queryset=TeamSquad.objects.all(), label="Squad ", required=True, empty_label="(Nothing)")

    class Meta:
        model = TeamSquad
        fields = ('listOfSquads', )


class TeamDeleteForm(ModelForm):
    listOfTeams = forms.ModelChoiceField(queryset=Team.objects.all(), label="Team ", required=True, empty_label="(Nothing)")

    class Meta:
        model = Team
        fields = ('listOfTeams', )


class TournamentForm(ModelForm):

    class Meta:
        model = Tournament
        widgets = {
          'startingDate': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
          'endingDate': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['startingDate'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['endingDate'].input_formats = ('%Y-%m-%dT%H:%M',)


class TournamentEditForm(ModelForm):
    listOfTournaments = forms.ModelChoiceField(queryset=Tournament.objects.all(), label="Tournament ", required=True, empty_label="(Nothing)")
    stage = forms.ModelChoiceField(queryset = Stage.objects.all(), label = "Stage ")
    winner = forms.ModelChoiceField(queryset = Team.objects.all(), label = "Team ")

    class Meta:
        model = Tournament
        widgets = {
          'startingDate': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
          'endingDate': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ('listOfTournaments', 'name', 'stage', 'startingDate', 'endingDate', 'winner', 'stateChoice', )

    def __init__(self, *args, **kwargs):
        super(TournamentEditForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['startingDate'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['endingDate'].input_formats = ('%Y-%m-%dT%H:%M',)


class TournamentDeleteForm(ModelForm):
    listOfTournaments = forms.ModelChoiceField(queryset=Tournament.objects.all(), label="Tournament ", required=True, empty_label="(Nothing)")

    class Meta:
        model = Tournament
        fields = ('listOfTournaments', )

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())


class StageDeleteForm(ModelForm):
    listOfStages = MyModelChoiceField(queryset = Stage.objects.all(), label = "Stage ", required = False, empty_label = None)
    class Meta:
        model = Stage
        fields = ('listOfStages',)
        
class MatchCreateForm(ModelForm):
    team1 = forms.ModelChoiceField(queryset = Team.objects.all(), required=True, empty_label="(None)", label='Team no.1', help_text='Required')
    team2 = forms.ModelChoiceField(queryset = Team.objects.all(), required=True, empty_label="(None)", label='Team no.2', help_text='Required') 
    date = forms.DateField(help_text='e.g. 2019-01-01 (YYYY-MM-DD)')
    class Meta:
        model = Match
        fields = ('team1','team2','date',)

class PlayerCreateForm(ModelForm):
    name = forms.CharField(max_length=20, required = True, label='Name', help_text='Required')
    secondName = forms.CharField(max_length=20, required = True, label='Second name', help_text='Required')
    role = forms.CharField(max_length=20, label='Role', required = False)
    birthDate = forms.DateField(help_text='e.g. 2019-01-01 (YYYY-MM-DD)')
    height = forms.IntegerField(label='Height (cm)', required = False, min_value=150)
    class Meta:
        model=Player
        fields=('name','secondName','role','birthDate','height',)

class MatchEditForm(ModelForm):
    listOfMatches = forms.ModelChoiceField(queryset=Match.objects.all(), label="Match", required=True, empty_label="(None)")
    date = forms.DateField(help_text='e.g. 2019-01-01 (YYYY-MM-DD)')
    points = forms.IntegerField(label="Goals scored by team 1", required=True, min_value=0)
    points2 = forms.IntegerField(label="Goals scored by team 2", required=True, min_value=0)
    class Meta:
        model=Match
        fields=['listOfMatches', 'date', 'points', 'points2']

class PlayerEditForm(ModelForm):
    listOfPlayers = forms.ModelChoiceField(queryset = Player.objects.all(), label = "Player", required = True, empty_label ="(None)")
    name = forms.CharField(max_length=20, required = True, label='Name')
    secondName = forms.CharField(max_length=20, required = True, label='Second name')
    role = forms.CharField(max_length=20, label='Role')
    birthDate = forms.DateField(help_text='e.g. 2019-01-01 (YYYY-MM-DD)')
    height = forms.IntegerField(label='Height (cm)', min_value=150)
    numberOfGoals = forms.IntegerField(label='Scored Goals', min_value=0)
    class Meta:
        model = Player
        fields=['listOfPlayers', 'name', 'secondName', 'role', 'birthDate', 'height', 'numberOfGoals']

class PlayerDeleteForm(ModelForm):
    listOfPlayers = forms.ModelChoiceField(queryset = Player.objects.all(), label = "Player", required = True, empty_label ="(None)")
    class Meta:
        model = Player
        fields = ('listOfPlayers',)

class MatchDeleteForm(ModelForm):
    listOfMatches = forms.ModelChoiceField(queryset = Match.objects.all(), label = "Match", required = True, empty_label ="(None)")
    class Meta:
        model = Match
        fields = ('listOfMatches',)

class ShootersForm(ModelForm):
    listOfMatches = forms.ModelChoiceField(queryset = Match.objects.all(), label = "Match", required = True, empty_label ="(None)")
    listOfPlayers = forms.ModelChoiceField(queryset = Player.objects.all(), label = "Player", required = True, empty_label ="(None)")
    goals = forms.IntegerField(label='Number of shot goals', min_value=1)
    class Meta:
        model = ShootersMatch
        fields = ('listOfMatches','listOfPlayers','goals')
