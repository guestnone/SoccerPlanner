"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from app.models import Player, TeamSquad, Team, Stage, Match, Event
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
    name = forms.CharField(max_length = 20, required= False, help_text='Required')
    listOfMatches = forms.ModelChoiceField(queryset = Match.objects.all(), label = "Match ")
    class Meta:
        model = Stage
        listOfMatches = [Match]
        fields = ('name','listOfMatches')


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name + " "+ obj.listOfMatches.team1.name + " " + obj.listOfMatches.team2.name


class StageEditForm(ModelForm):
    listOfStages = MyModelChoiceField(queryset = Stage.objects.all(), label = "Stage ", required = True, empty_label= None)
    listOfMatches = forms.ModelChoiceField(queryset = Match.objects.all(), label = "Match ")
    class Meta:
        model = Stage
        fields = ('listOfStages','name','listOfMatches')

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

class StageDeleteForm(ModelForm):
    listOfStages = MyModelChoiceField(queryset = Stage.objects.all(), label = "Stage ", required = True, empty_label = None)
    class Meta:
        model = Stage
        fields = ('listOfStages',)
        
class TeamSquadForm(ModelForm):
    name = forms.CharField(max_length=20, required=True, help_text='Required.')
    playerID = forms.ModelChoiceField(queryset=Player.objects.all(), label="Player ", required=True, empty_label="(Nothing)")

    class Meta:
        model = TeamSquad
        fields = ('playerID', 'name', )


class TeamForm(ModelForm):
    name = forms.CharField(max_length=20, required=True, help_text='Required.')
    country = forms.CharField(max_length=20, required=True, help_text='Required.')
    squad = forms.ModelChoiceField(queryset=TeamSquad.objects.all(), required=True, empty_label="(Nothing)")

    class Meta:
        model = Team
        fields = ('name', 'country', 'squad', )


class TeamSquadEditForm(ModelForm):
    listOfSquads = forms.ModelChoiceField(queryset=TeamSquad.objects.all(), label="Squad ", required=True, empty_label="(Nothing)")
    playerID = forms.ModelChoiceField(queryset=Player.objects.all(), label="Player ", required=True, empty_label="(Nothing)")

    class Meta:
        model = TeamSquad
        fields = ('listOfSquads', 'name', 'playerID', )


class TeamEditForm(ModelForm):
    listOfTeams = forms.ModelChoiceField(queryset=Team.objects.all(), label="Team ", required=True, empty_label="(Nothing)")
    squad = forms.ModelChoiceField(queryset=TeamSquad.objects.all(), required=True, empty_label="(Nothing)")

    class Meta:
        model = Team
        fields = ('listOfTeams', 'name', 'country', 'squad', )

