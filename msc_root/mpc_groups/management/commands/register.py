from django.core.management.base import BaseCommand, CommandError
from mpc_groups.models import MpcAdminRegistration

class Command(BaseCommand):
    help = 'Processes registrations'

    def __init__(self):
        self._groups = {}
    
    def handle(self, *args, **options):
        # TODO Fill in _groups
        registrations = MpcAdminRegistration.objects.all()
        for registration in registrations:
            self.register(registration.primary_group)
            if registration.secondary_group:
                self.register(registration.secondary_group)
    
    def register(self, group_name):
        cannonical = group_name.strip().lower()
        if cannonical not in self._groups:
            self._groups[cannonical] = group_name.strip()
            print(group_name.strip())
        else:
            print("DUP")