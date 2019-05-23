"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from app.models import Player, TeamSquad, Team, Stage, Match, Players, Matches
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView
#from snowpenguin.django.recaptcha2.fields import ReCaptchaField
#from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

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

class MatchEditForm(forms.Form):
    listOfTeams = forms.ModelChoiceField(queryset=Match.objects.all(), label="Match", required=True, empty_label="(None)")
    date = forms.DateField(help_text='e.g. 2019-01-01 (YYYY-MM-DD)')
    points = forms.IntegerField(label="Goals scored by team 1", required=True, min_value=0)
    points2 = forms.IntegerField(label="Goals scored by team 2", required=True, min_value=0)
    class Meta:
        model=Match
        fields=('listOfTeams', 'points', 'points2', 'date',)

class PlayerEditForm(forms.Form):
    listOfPlayers = forms.ModelChoiceField(queryset=Player.objects.all(), label="Player", required=True, empty_label="(None)")
    name = forms.CharField(max_length=20, required = True, label='Name')
    secondName = forms.CharField(max_length=20, required = True, label='Second name')
    role = forms.CharField(max_length=20, label='Role')
    birthDate = forms.DateField(help_text='e.g. 2019-01-01 (YYYY-MM-DD)')
    height = forms.IntegerField(label='Height (cm)', min_value=150)
    numberOfGoals = forms.IntegerField(label='Scored Goals', min_value=0)
    class Meta:
        model=Player
        fields=('listOfPlayers','name','secondName','role','birthDate','height','numberOfGoals')

class PlayerDeleteForm(ModelForm):
    listOfPlayers = forms.ModelChoiceField(queryset = Player.objects.all(), label = "Player", required = True, empty_label ="(None)")
    class Meta:
        model = Players
        fields = ('listOfPlayers',)

class MatchDeleteForm(ModelForm):
    listOfMatches = forms.ModelChoiceField(queryset = Match.objects.all(), label = "Match", required = True, empty_label ="(None)")
    class Meta:
        model = Matches
        fields = ('listOfMatches',)