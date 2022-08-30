from concurrent.futures.process import _threads_wakeups
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from mpc_groups.models import MpcGroup
from teams.models import Team

class Profile(models.Model):
    peaker = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    group = models.ForeignKey(MpcGroup, null=True, blank=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(peaker=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        pass  # Don't need to update if we don't have one, such as for admin.

class StepEntry(models.Model):
    peaker = models.ForeignKey(User, on_delete=models.CASCADE)
    entered = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    steps = models.IntegerField()
    valid = models.BooleanField()
    notes = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['peaker','date'], name='One Entry for day in Septemberpy')
        ]

    def __str__(self):
        return str(self.peaker) + " " + str(self.date)

    def clean(self):
        # Validation here
        self.valid = True