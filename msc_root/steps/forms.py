from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import StepEntry
from mpc_groups.models import MpcGroup

class StepEntryForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = StepEntry
        fields = [
            'date', 'steps'
        ]

class PeakerRegistrationForm(UserCreationForm):
    group_field = forms.ModelChoiceField(label='Ambassador Group', queryset=MpcGroup.objects.all().order_by('name'), empty_label='None, pick a Team for me.', required=False)
    class Meta(UserCreationForm.Meta):
        pass
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
