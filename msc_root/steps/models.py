from concurrent.futures.process import _threads_wakeups
from django.db import models
from django.contrib.auth.models import User

class StepEntry(models.Model):
    peaker = models.ForeignKey(User, on_delete=models.CASCADE)
    entered = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    steps = models.FloatField()
    valid = models.BooleanField()
    notes = models.TextField()

    def __str__(self):
        return str(self.peaker) + " " + str(self.date)

    def clean(self):
        # Validation here
        self.valid = True