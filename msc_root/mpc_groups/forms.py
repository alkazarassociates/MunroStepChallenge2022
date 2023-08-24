from django import forms
from django.conf import settings
from django.forms import ModelForm
from .models import MpcAdminRegistration

class MpcAdminRegistrationForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = MpcAdminRegistration
        fields = [
            'name', 'primary_group',
        ]
        if settings.CURRENT_PHASE.allow_2_groups_per_admin():
            fields.append('secondary_group')