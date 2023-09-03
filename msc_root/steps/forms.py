from sqlite3 import Date
import datetime
from xml.dom import ValidationErr
from django.conf import settings
from django.core.mail import EmailMessage
from django import forms
from django.forms import ModelForm, ValidationError, DateField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy, gettext as _
from .models import Profile, StepEntry
from .tokens import account_activation_token
from mpc_groups.models import MpcGroup

class StepEntryForm(ModelForm):
    required_css_class = 'required'
    date = forms.DateField(widget=forms.SelectDateWidget, label=gettext_lazy('Date'))
    class Meta:
        model = StepEntry
        fields = [
            'date', 'steps'
        ]
        labels = {
            'steps': gettext_lazy('Steps')
        }
    
    def clean_date(self):
        d = self.cleaned_data['date']
        if d < settings.CURRENT_PHASE.challenge_start_date or d >= settings.CURRENT_PHASE.challenge_end_date:
            raise ValidationError(_("Steps must be for the month of September"))
        # UTC+-12 should be enough of the world for this.
        if datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+12))).date() < d:
            raise ValidationError(_("You can't enter steps for the future"))
        if datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-12))).date() > d + datetime.timedelta(days=7.0):
            raise ValidationError(_("You can't enter steps more than a week old"))
        return d

    def clean_steps(self):
        s = self.cleaned_data['steps']
        if s < 0:
            raise ValidationError(_("You must enter a positive number of steps"))
        return s


class PeakerRegistrationForm(UserCreationForm):
    email = forms.EmailField(label=_('Email'), help_text=_('We use this to contact you for reset passwords only!'))
    group_field = forms.ModelChoiceField(label=_('Ambassador Group'),
                                         queryset=MpcGroup.objects.all().order_by('name') if settings.CURRENT_PHASE.allow_registration_in_group else MpcGroup.objects.none(),
                                         empty_label=_('None, pick a Team for me.') if settings.CURRENT_PHASE.allow_non_group_peakers else _("--- Select Ambassador Group ---"), required=not settings.CURRENT_PHASE.allow_non_group_peakers, 
                                         help_text=_('We will make sure you are on the same Team as this the rest of the group'))
    class Meta(UserCreationForm.Meta):
        pass
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        isnew = User.objects.filter(username=username)
        if isnew.count():
            raise ValidationError(_("User already exists"))
        return username
    
    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        isnew = User.objects.filter(email=email)
        if isnew.count():
            raise ValidationError(_("Email already registered"))
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
            _('Confirm email  for ') + _(settings.CURRENT_PHASE.challenge_name),
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
        fields = [ 'fundraising', 'imperial']
        help_texts = {'fundraising': "Select 'do not count' if you wish to fundraise with your own steps separately, or not fundraise with them for other reasons."}
