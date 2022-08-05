from concurrent.futures.process import _threads_wakeups
from django.db import models
from django.contrib.auth.models import User

WALK = 'W'
SWIM = 'S'
BIKE = 'B'

ACTIVITIES = (
    (WALK,'Walk/Run'),
    (SWIM, 'Swim'),
    (BIKE, 'Bike'),
)
class StepEntry(models.Model):
    peaker = models.ForeignKey(User, on_delete=models.CASCADE)
    entered = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    activity = models.CharField(max_length=1, choices=ACTIVITIES, default=WALK)
    amount = models.FloatField()
    valid = models.BooleanField()

    def __str__(self):
        return str(self.peaker) + " " + str(self.date)

    def clean(self):
        # Validation here
        self.valid = True