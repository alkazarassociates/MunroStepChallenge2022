from concurrent.futures.process import _threads_wakeups
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from mpc_groups.models import MpcGroup
from teams.models import Team

# TODO 2023 Add time zone.
class Profile(models.Model):
    peaker = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    group = models.ForeignKey(MpcGroup, null=True, blank=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
    TSC_FUNDRAISING='TSC'
    OTHER_FUNDRAISING='NO'
    FUNDRAISING_CHOICES = [
        (TSC_FUNDRAISING, "Count my steps towards my group's fundraising"),
        (OTHER_FUNDRAISING, "Do not count my steps towards my group's fundraising.")
    ]
    fundraising = models.CharField(max_length=3, choices=FUNDRAISING_CHOICES, default=TSC_FUNDRAISING)
    imperial = models.BooleanField(verbose_name='USA Units', default=True, help_text=_("Check means distances are miles, unchecked means kilometers."))

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
    steps = models.IntegerField(help_text=_("No ',' or '.' please. Just digits."))
    valid = models.BooleanField()
    notes = models.TextField(default='', blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['peaker','date'], name='One Entry for day in September')
        ]

    def __str__(self):
        return str(self.peaker) + " " + str(self.date)

    def clean(self):
        # Validation here
        self.valid = True