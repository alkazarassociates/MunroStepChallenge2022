from django.db import models

class Team(models.Model):
    name = models.CharField('Name', max_length=16, unique=True)
    description = models.TextField('Description')
    color = models.CharField('Color', max_length=20, default='Black')

    def __str__(self):
        return self.name
