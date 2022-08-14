from django.db import models
from teams.models import Team

class MpcGroup(models.Model):
    name = models.CharField('Name', max_length=60, unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    admin = models.CharField('Admin', max_length=60)

    def __str__(self):
        return self.name

class MpcAdminRegistration(models.Model):
    name = models.CharField('Name', max_length=40, help_text="Enter the facebook name you use.")
    primary_group = models.CharField('Ambassador Group', max_length=60, help_text="Enter the name of your Ambassador Group as you wish it to appear.")
    secondary_group = models.CharField('Optional Additional Group', max_length=60, blank=True, help_text="If you are the admin of another group, you can enter it here to request your two groups be on the same Team.")

    def __str__(self):
        sep = ''
        if self.secondary_group:
            sep = ' & '
        return f'{self.name}:{self.primary_group}{sep}{self.secondary_group}'

class GroupModifications(models.Model):
    modification_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.modification_time.strftime("%m/%d/%Y %H:%M")