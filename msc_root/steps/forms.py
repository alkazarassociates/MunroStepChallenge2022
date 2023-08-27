from sqlite3 import Date
import datetime
from xml.dom import ValidationErr
from django.conf import settings
from django.core.mail import EmailMessage
from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Profile, StepEntry
from .tokens import account_activation_token
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
    email = forms.EmailField(label='Email', help_text='We use this to contact you for reset passwords only!')
    group_field = forms.ModelChoiceField(label='Ambassador Group',
                                         queryset=MpcGroup.objects.all().order_by('name') if settings.CURRENT_PHASE.allow_registration_in_group else MpcGroup.objects.none(),
                                         empty_label='None, pick a Team for me.', required=False)
    class Meta(UserCreationForm.Meta):
        pass
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        isnew = User.objects.filter(username=username)
        if isnew.count():
            raise ValidationError("User already exists")
        return username
    
    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        isnew = User.objects.filter(email=email)
        if isnew.count():
            raise ValidationError("Email already registered")
        return email
    
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        user.is_active = False
        user.save()  # is_active is getting set true without this.
        message = render_to_string('registration/acc_active_email.html', 
                                   {'user': user,
                                    'domain': settings.CURRENT_PHASE.domain,
                                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token':account_activation_token.make_token(user)})
        email = EmailMessage(
            'Confirm email  for ' + settings.CURRENT_PHASE.challenge_name,
            message, from_email=settings.EMAIL_OUR_ADDRESS, to=[self.cleaned_data['email']])
        email.send()
        return user
    

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
