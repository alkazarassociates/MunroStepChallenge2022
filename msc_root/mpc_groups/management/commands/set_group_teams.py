import json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
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
        print()
        for peaker in User.objects.all():
            if hasattr(peaker, 'profile') and peaker.profile.group:
                print(f"Peaker {peaker.username} in {peaker.profile.group} to Team {peaker.profile.group.team}")
                peaker.profile.team = peaker.profile.group.team
                peaker.save()