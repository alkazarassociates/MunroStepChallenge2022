from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from steps.models import Profile

class Command(BaseCommand):
    help = 'Set Group Teams'

    def handle(self,*args, **options):
        for user in User.objects.order_by('username'):
            if not Profile.objects.filter(peaker=user).exists():
                print(user.username)