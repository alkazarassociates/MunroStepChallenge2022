from django.db import models

class Team(models.Model):
    name = models.CharField('Name', max_length=16, unique=True)

    def __str__(self):
        return self.name
