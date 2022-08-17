from django import forms
from django.forms import ModelForm
from .models import StepEntry

class StepEntryForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = StepEntry
        fields = [
            'date', 'steps'
        ]