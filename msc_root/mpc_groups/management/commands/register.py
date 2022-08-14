from django.core.management.base import BaseCommand, CommandError
from mpc_groups.models import MpcAdminRegistration, MpcGroup

class Command(BaseCommand):
    help = 'Processes registrations'

    def __init__(self):
        self._groups = {}
    
    def handle(self, *args, **options):
        # TODO Fill in _groups
        registrations = MpcAdminRegistration.objects.all()
        for registration in registrations:
            self.register(registration.primary_group, registration.name)
            if registration.secondary_group:
                self.register(registration.secondary_group, registration.name)
    
    def register(self, group_name, admin):
        cannonical = group_name.strip().lower()
        if cannonical not in self._groups:
            group_name = group_name.strip()
            MpcGroup.objects.update_or_create(name=group_name, admin=admin.strip())
            self._groups[cannonical] = group_name
            print(group_name)
        else:
            obj = MpcGroup.objects.get(name=group_name.strip())
            old = obj.admin
            obj.admin = admin.strip()
            obj.save()
            print(f"DUP: changed admin from {old} to {admin.strip()}")