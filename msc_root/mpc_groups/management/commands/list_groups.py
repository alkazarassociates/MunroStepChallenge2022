from collections import defaultdict
import json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mpc_groups.models import MpcGroup
from teams.models import Team

class Command(BaseCommand):
    help = 'List Groups and their sizes'

    def handle(self, *args, **options):
        counter = defaultdict(int)
        for peaker in User.objects.all():
            if hasattr(peaker, 'profile') and peaker.profile.group:
                 counter[peaker.profile.group] += 1
        print("GROUP, member count")
        for g in counter:
            print(f"{g}, {counter[g]}")