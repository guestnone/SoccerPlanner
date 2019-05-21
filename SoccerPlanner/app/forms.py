"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import Player, TeamSquad, Team
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView


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
