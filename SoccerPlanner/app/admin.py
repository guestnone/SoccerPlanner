from django.contrib import admin
from .models import Player, TeamSquad, Team
from app.models import *

admin.site.register(Player)
admin.site.register(TeamSquad)
admin.site.register(Team)
admin.site.register(Event)
admin.site.register(Match)
admin.site.register(ShootersMatch)
