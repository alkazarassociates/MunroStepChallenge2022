from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from steps.models import Profile
from teams.models import Team

class Command(BaseCommand):
    help = 'Set Group Teams'

    def add_arguments(self, parser) -> None:
        parser.add_argument('--fix', action='store_true')

    def handle(self,*args, **options):
        c = 0
        for user in User.objects.order_by('username'):
            if user.username == 'admin': 
                continue
            if not Profile.objects.filter(peaker=user).exists():
                print(user.username)
                if options['fix']:
                    prof = Profile(peaker=user, team=Team.objects.filter(name='Beech').get())
                    prof.save()
                c += 1
        print(f"Total of {c} broken users")