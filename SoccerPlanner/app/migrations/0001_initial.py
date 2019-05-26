
# Generated by Django 2.2.1 on 2019-05-24 16:28


from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('MatchID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('points', models.IntegerField(default=0)),
                ('points2', models.IntegerField(default=0)),
                ('date', models.DateField(default='2019-01-01')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('playerID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('secondName', models.CharField(max_length=20)),
                ('role', models.CharField(max_length=20)),
                ('birthDate', models.DateField(default='2019-01-01')),
                ('height', models.IntegerField(default=180)),
                ('numberOfGoals', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startingDate', models.DateTimeField(verbose_name='Starting date')),
                ('endingDate', models.DateTimeField(verbose_name='Ending date')),
                ('stateChoice', models.CharField(choices=[('BF', 'Before'), ('IP', 'In progress'), ('PL', 'Played'), ('CN', 'Cancelled')], default='BF', max_length=2)),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamSquad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('name', models.CharField(default='', max_length=20)),

                ('playerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Player')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='squad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.TeamSquad'),
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('listOfMatches', models.ManyToManyField(to='app.Match')),
            ],
        ),
        migrations.CreateModel(
            name='ShootersMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', models.IntegerField(default=0)),
                ('playerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Player')),
            ],
        ),
        migrations.CreateModel(
            name='ShooterRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ShootersMatch')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='shootersPerMatch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ShootersMatch'),
        ),
        migrations.AddField(
            model_name='match',
            name='team1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='app.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='app.Team'),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(help_text='Day of the event', verbose_name='Day of the event')),
                ('start_time', models.DateTimeField(help_text='Starting time', verbose_name='Starting time')),
                ('end_time', models.DateTimeField(help_text='Final time', verbose_name='Final time')),
                ('notes', models.TextField(blank=True, help_text='Textual Notes', null=True, verbose_name='Textual Notes')),
                ('linkedMatch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Match')),
            ],
            options={
                'verbose_name': 'Scheduling',
                'verbose_name_plural': 'Scheduling',
            },
        ),
    ]
