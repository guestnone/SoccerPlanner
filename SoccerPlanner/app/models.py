"""
Definition of models.
"""

import uuid

from django.db import models

from django.db.models import ForeignKey
from django.urls import reverse


class Player(models.Model):
    playerID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=20)
    secondName = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    birthDate = models.DateTimeField("Birth Date")
    height = models.IntegerField(default=0)
    numberOfGoals = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.secondName


class TeamSquad(models.Model):
    name = models.CharField(max_length=20)
    playerID = models.ManyToManyField(Player, verbose_name="list of players")

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    squad = ForeignKey(TeamSquad, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Match(models.Model):
    MatchID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    team1 = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, related_name="team1"
    )
    team2 = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, related_name="team2"
    )
    points = models.IntegerField(default=0, null=True, blank=True)
    points2 = models.IntegerField(default=0, null=True, blank=True)
    # shootersPerMatch = models.ForeignKey(ShootersMatch, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.team1.name + " " + self.team2.name


class ShootersMatch(models.Model):
    shootID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    listOfMatches = models.ForeignKey(
        Match, on_delete=models.CASCADE, null=True, blank=True
    )
    listOfPlayers = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True, blank=True
    )
    goals = models.IntegerField(default=0, null=True, blank=True)


# class ShooterRank(models.Model):
#    playerID = models.ForeignKey(ShootersMatch, on_delete=models.CASCADE)


class Stage(models.Model):
    name = models.CharField(max_length=80)
    listOfMatches = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):
        return (
            self.name
            + " "
            + self.listOfMatches.team1.name
            + " "
            + self.listOfMatches.team2.name
        )


class Tournament(models.Model):
    name = models.CharField(max_length=80, default="")
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True)
    startingDate = models.DateTimeField("Starting date")
    endingDate = models.DateTimeField("Ending date")
    winner = models.ForeignKey(Team, on_delete=models.CASCADE)

    BEFORE = "BF"
    IN_PROGRESS = "IP"
    PLAYED = "PL"
    CANCELLED = "CN"

    STATE_CHOICES = (
        (BEFORE, "Before"),
        (IN_PROGRESS, "In progress"),
        (PLAYED, "Played"),
        (CANCELLED, "Cancelled"),
    )
    stateChoice = models.CharField(max_length=2, choices=STATE_CHOICES, default=BEFORE)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.TextField("Event Name", blank=True, null=True)
    day = models.DateField("Day of the event", help_text="Day of the event")
    start_time = models.DateTimeField("Starting time", help_text="Starting time")
    end_time = models.DateTimeField("Final time", help_text="Final time")
    notes = models.TextField(
        "Textual Notes", help_text="Textual Notes", blank=True, null=True
    )
    linkedMatch = models.ForeignKey(Match, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Scheduling"
        verbose_name_plural = "Scheduling"

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (
            new_end >= fixed_start and new_end <= fixed_end
        ):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=[self.id],
        )
        return '<a href="%s">%s</a>' % (url, str(self.start_time))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("Ending hour must be after the starting hour")

    @property
    def get_html_url(self):
        url = reverse("event_edit", args=(self.id,))
        return f'<a href="{url}"> {self.notes} </a>'
