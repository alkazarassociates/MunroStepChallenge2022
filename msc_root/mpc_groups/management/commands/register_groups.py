from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User 
from mpc_groups.models import MpcAdminRegistration, MpcGroup, GroupModifications
from teams.models import Team

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False


class Command(BaseCommand):
    help = 'Processes registrations'

    def __init__(self):
        self._groups = {}
    
    def handle(self, *args, **options):
        self.update_groups()
        registrations = MpcAdminRegistration.objects.all()
        for registration in registrations:
            self.register(registration.primary_group, registration.name)
            if registration.secondary_group:
                self.register(registration.secondary_group, registration.name)
    
    def register(self, group_name, admin):
        modified = False
        cannonical = group_name.strip().lower()
        if cannonical not in self._groups:
            group_name = group_name.strip()
            if not MpcGroup.objects.filter(name=group_name).exists():
                if yes_or_no(f"Create '{group_name}'?"):
                    if settings.CURRENT_PHASE.teams_assigned():
                        # We need to calculate what team to put this group on.
                        counter = {}
                        for team in Team.objects.filter(auxiliary=True):
                            counter[team] = User.objects.filter(profile__team=team).count()
                        team = min(counter, key=counter.get)
                    else:
                        team = Team.UnassignedTeam()
                    MpcGroup.objects.update_or_create(name=group_name, admin=admin.strip(), team=team)
                    modified = True
                    print(group_name)
            self._groups[cannonical] = group_name
        elif settings.CURRENT_PHASE.allow_group_modifications():
            print(group_name.strip())
            obj = MpcGroup.objects.get(name=self._groups[group_name.strip().lower()])
            old = obj.admin
            obj.admin = admin.strip()
            if obj.admin != old:
                obj.save()
                print(f"DUP: changed admin from {old} to {admin.strip()}")
                modified = True
        else:
            pass
        if modified or GroupModifications.objects.count() == 0:
            GroupModifications.objects.create()


    def update_groups(self):
        self._groups = {}
        for g in MpcGroup.objects.all():
            self._groups[g.name.lower()] = g.name