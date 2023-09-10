import csv
import datetime
import os.path

from django.core.management.base import BaseCommand
from django.db.models import Sum
from mpc_groups.models import MpcGroup
from steps.models import StepEntry
from teams.models import Team

class Command(BaseCommand):
    help = 'Print Team Totals'

    def add_arguments(self, parser) -> None:
        parser.add_argument('day', type=int)

    def handle(self, *args, **options):
        today = datetime.date.today()
        with open('team_data.csv', 'w', newline='') as out:
            cutoff = datetime.date(today.year, today.month, options['day'])
            print(f"Total of steps on or before {cutoff} as entered at {datetime.datetime.now()}", file=out)
            w = csv.writer(out)
            team_list = Team.objects.order_by('name').all()
            w.writerow(['Day', 'Total'] + [team.name for team in team_list])
            for day in range(1, options['day'] + 1):
                cutoff = datetime.date(today.year, today.month, day)
                all_teams_total = 0
                team_totals = []
                for team in team_list:
                    step_total = StepEntry.objects.filter(date__lte=cutoff, peaker__profile__team=team).aggregate(Sum('steps'))['steps__sum'] or 0
                    team_totals.append(step_total)
                    all_teams_total += step_total
                w.writerow([day, all_teams_total] + team_totals)
        with open('group_data.csv', 'w', newline='') as out:
            cutoff = datetime.date(today.year, today.month, options['day'])
            print(f"Total of steps on or before {cutoff} as entered at {datetime.datetime.now()}", file=out)
            w = csv.writer(out)
            for team in team_list:
                w.writerow(['TEAM ' + team.name, 'Total'])
                for group in MpcGroup.objects.filter(team=team).order_by('name'):
                    step_total = StepEntry.objects.filter(date__lte=cutoff, peaker__profile__group=group).aggregate(Sum('steps'))['steps__sum'] or 0
                    w.writerow([group.name, step_total])
                w.writerow([])