from django.db import models
from teams.models import Team

class Group(models.Model):
    name = models.CharField('Name', max_length=40, unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    # TODO Admins, many_to_many to users with admin=true

    def __str__(self):
        return self.name
