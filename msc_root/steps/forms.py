from sqlite3 import Date
import datetime
from xml.dom import ValidationErr
from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, StepEntry
from mpc_groups.models import MpcGroup

class StepEntryForm(ModelForm):
    required_css_class = 'required'
    date = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = StepEntry
        fields = [
            'date', 'steps'
        ]
    
    def clean_date(self):
        d = self.cleaned_data['date']
        if d < datetime.date(2022, 9, 1) or d >= datetime.date(2022, 10, 1):
            raise ValidationError("Steps must be for the month of September")
        # UTC+-12 should be enough of the world for this.
        if datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+12))).date() < d:
            raise ValidationError("You can't enter steps for the future")
        if datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-12))).date() > d + datetime.timedelta(days=7.0):
            raise ValidationError("You can't enter steps more than a week old")
        return d

    def clean_steps(self):
        s = self.cleaned_data['steps']
        if s < 0:
            raise ValidationError("You must enter a possitive number of steps")
        return s


class PeakerRegistrationForm(UserCreationForm):
    group_field = forms.ModelChoiceField(label='Ambassador Group', queryset=MpcGroup.objects.all().order_by('name'), empty_label='None, pick a Team for me.', required=False)
    class Meta(UserCreationForm.Meta):
        pass
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PeakerModificationForm(ModelForm):
    group = forms.ModelChoiceField(label='Group', queryset=MpcGroup.objects.all().order_by('name'), empty_label='None, pick a Team for me.', required=False)
    required_css_class = 'required'
    class Meta:
        model = Profile
        fields = [ 'group' ]
