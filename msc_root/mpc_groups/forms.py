from django import forms
from django.forms import ModelForm
from .models import MpcAdminRegistration

class MpcAdminRegistrationForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = MpcAdminRegistration
        fields = [
            'name', 'primary_group', 'secondary_group'
        ]