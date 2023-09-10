import datetime

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
        cutoff = datetime.date(today.year, today.month, options['day'])
        print(f"Total of steps on or before {cutoff} as entered at {datetime.datetime.now()}")
        all_teams_total = 0
        for team in Team.objects.order_by('name'):
            step_total = StepEntry.objects.filter(date__lte=cutoff, peaker__profile__team=team).aggregate(Sum('steps'))['steps__sum'] or 0
            print(f"Team {team.name},{step_total}")
            all_teams_total += step_total
        print(f"ALL,{all_teams_total}")
        print()
        for group in MpcGroup.objects.order_by('name'):
            step_total = StepEntry.objects.filter(date__lte=cutoff, peaker__profile__group=group).aggregate(Sum('steps'))['steps__sum'] or 0
            print(f"{group.name},{step_total}")
