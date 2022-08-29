import json

from django.core.management.base import BaseCommand
from mpc_groups.models import MpcGroup
from teams.models import Team

class Command(BaseCommand):
    help = 'Set Group Teams'

    def add_arguments(self, parser) -> None:
        parser.add_argument('assignment_file', type=open)

    def handle(self, *args, **options):
        assignments = json.load(options['assignment_file'])
        for g in assignments:
            print(f"Group {g} to Team {assignments[g]}")
            group = MpcGroup.objects.get(name=g)
            group.team = Team.objects.get(name=assignments[g])
            group.save()