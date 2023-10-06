import csv
import datetime
import os.path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Sum
from mpc_groups.models import MpcGroup
from steps.models import StepEntry, Profile
from teams.models import Team

class Command(BaseCommand):
    help = 'Print Team Totals'

    def add_arguments(self, parser) -> None:
        parser.add_argument('day', type=int)
        parser.add_argument('--cut', action='store_true')  # TODO Make cut time configurable

    def handle(self, *args, **options):
        today = datetime.date.today()
        cut = datetime.datetime.now(tz=datetime.timezone.utc)
        if options['cut']:
            cut = datetime.datetime(2023, 10, 3, 20, 49, 13,862736, tzinfo=datetime.timezone.utc)
        with open('team_data.csv', 'w', newline='') as out:
            cutoff = settings.CURRENT_PHASE.challenge_start_date + datetime.timedelta(days=options['day'] - 1)
            print(f"Total of steps on or before {cutoff} as entered at {datetime.datetime.now()}", file=out)
            w = csv.writer(out)
            team_list = Team.objects.order_by('name').all()
            w.writerow(['Day', 'Total'] + [team.name for team in team_list])
            for day in range(1, options['day'] + 1):
                cutoff = settings.CURRENT_PHASE.challenge_start_date + datetime.timedelta(days=day-1)
                all_teams_total = 0
                team_totals = []
                for team in team_list:
                    step_total = StepEntry.objects.filter(date__lte=cutoff, entered__lte=cut, peaker__profile__team=team).aggregate(Sum('steps'))['steps__sum'] or 0
                    team_totals.append(step_total)
                    all_teams_total += step_total
                w.writerow([day, all_teams_total] + team_totals)
        with open('team_group.csv', 'w', newline='') as out:
            cutoff = settings.CURRENT_PHASE.challenge_start_date + datetime.timedelta(days=options['day'] - 1)
            print(f"Total of steps on or before {cutoff} as entered at {datetime.datetime.now()}", file=out)
            w = csv.writer(out)
            for team in team_list:
                w.writerow(['TEAM ' + team.name, 'Total', 'Participants'])
                for group in MpcGroup.objects.filter(team=team).order_by('name'):
                    step_total = StepEntry.objects.filter(date__lte=cutoff, entered__lte=cut, peaker__profile__group=group).aggregate(Sum('steps'))['steps__sum'] or 0
                    participants = StepEntry.objects.filter(date__lte=cutoff, entered__lte=cut, peaker__profile__group=group).distinct('peaker').count()
                    w.writerow([group.name, step_total, participants])
                w.writerow([])
        with open('group_data.csv', 'w', newline='') as out:
            cutoff = settings.CURRENT_PHASE.challenge_start_date + datetime.timedelta(days=options['day'] - 1)
            print(f"Total of steps on or before {cutoff} as entered at {datetime.datetime.now()}", file=out)
            w = csv.writer(out)
            w.writerow(['Group', 'Total', 'Participants'])
            for group in MpcGroup.objects.order_by('name'):
                step_total = StepEntry.objects.filter(date__lte=cutoff, entered__lte=cut, peaker__profile__group=group).aggregate(Sum('steps'))['steps__sum'] or 0
                participants = StepEntry.objects.filter(date__lte=cutoff, entered__lte=cut, peaker__profile__group=group).distinct('peaker').count()
                w.writerow([group.name, step_total, participants])
            w.writerow([])
        with open('participant_data.csv', 'w', newline='') as out:
            # depend on cutoff not changing.
            print(f"Total of steps on or before {cutoff} as entered at {datetime.datetime.now()}", file=out)
            w = csv.writer(out)
            w.writerow(['Participant', 'Group', 'Team', 'Total'])
            for peaker in StepEntry.objects.filter(date__lte=cutoff, entered__lte=cut).distinct('peaker'):
                profiles = Profile.objects.filter(pk=peaker.peaker)
                if profiles:
                    assert(len(profiles) == 1)
                    profile = profiles[0]
                    total = StepEntry.objects.filter(date__lte=cutoff, entered__lte=cut, peaker=peaker.peaker).aggregate(Sum('steps'))['steps__sum']
                    w.writerow([profile.peaker.username, profile.group.name, profile.team.name, total])
            w.writerow([])
