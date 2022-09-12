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
    group_field = forms.ModelChoiceField(label='Ambassador Group', queryset=MpcGroup.objects.none(), empty_label='None, pick a Team for me.', required=False)
    class Meta(UserCreationForm.Meta):
        pass
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PeakerModificationForm(ModelForm):
    # This code for disallowing group changes.
    #group = forms.ModelChoiceField(label='Group', queryset=MpcGroup.objects.none().order_by('name'), empty_label='None, pick a Team for me.', required=False)
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        current_group = kwargs.pop('current_group', None)
        super().__init__(*args, **kwargs)

        # When disallowing group switching, this code is how we can modify the drop down.
        #if current_group:
        # BUG: This seems for force the "pick a group for me", even when not intended.
        #    self.fields['group'].queryset = MpcGroup.objects.filter(pk=current_group)
    
    class Meta:
        model = Profile
        fields = [ 'imperial']
