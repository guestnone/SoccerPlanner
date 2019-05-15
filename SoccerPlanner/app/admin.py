from django.contrib import admin

from .models import Match,Stage,Player,Team, ShootersMatch, TeamSquad

admin.site.register(Match)
admin.site.register(Stage)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(ShootersMatch)
admin.site.register(TeamSquad)