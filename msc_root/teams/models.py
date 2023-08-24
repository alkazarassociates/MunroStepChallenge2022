from django.db import models

class Team(models.Model):
    name = models.CharField('Name', max_length=16, unique=True)
    description = models.TextField('Description')
    color = models.CharField('Color', max_length=20, default='Black')
    picture = models.CharField('Picture', max_length=40, blank=True, null=True)
    auxiliary = models.BooleanField('Auxiliary', default=False)

    def __str__(self):
        return self.name
    
    @staticmethod
    def UnassignedTeam():
        if Team.objects.exists():
            return Team.objects.first()
        else:
            raise Exception("Please create a placeholder team");