from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, base36_to_int
from django.utils.translation import gettext as _
from collections import defaultdict
import datetime
import urllib

from .models import Profile, StepEntry
from .forms import PeakerRegistrationForm, StepEntryForm, PeakerModificationForm
from .tokens import account_activation_token

from mpc_groups.models import MpcGroup
from teams.models import Team

class Register(CreateView):
            
    template_name: str = 'registration/register.html'
    form_class = PeakerRegistrationForm
    success_url = reverse_lazy('register-success')

    # TODO 2023
    # TimeZone.
    # More than one groups.

    def form_valid(self, form):
        form.save()
        # Now save the profile
        prof = Profile.objects.get(peaker=User.objects.get(username=form.cleaned_data['username']))
        prof.group=form.cleaned_data['group_field']
        if prof.group and prof.group.team:
            prof.team = prof.group.team
        if not prof.team:
            # We need to calculate what team to put this peaker on.
            counter = {}
            for team in Team.objects.filter(auxiliary=False):
                counter[team] = User.objects.filter(profile__team=team).count()
            prof.team = min(counter, key=counter.get)

        prof.save()
        return HttpResponseRedirect(self.success_url)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse_lazy('activate-success'))
    else:
        return HttpResponse(_("<p>Activation link is invalid, or account already avtivated.</p><p>This can happen if you click on activation link twice.  Try logging in.</p>"))


@login_required(login_url=reverse_lazy('login'))
def step_entry(request):
    submitted = False
    latest = None
    steps = StepEntry.objects.filter(peaker=request.user)
    if steps:
        latest = steps.latest('entered')
        d = latest.date.strftime("%B %d")
        recent_steps = _("{step_count} steps for {date}").format(step_count=latest.steps, date=d)
    else:
        recent_steps = ""
    activity = request.session.get('last_activity', '')
    if request.method == 'POST':
        form = StepEntryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['steps'] > 50000:
                return HttpResponseRedirect(f"/steps/large_entry?date={form.cleaned_data['date']}&steps={form.cleaned_data['steps']}")
            entry = form.save(commit=False)
            try:
                entry.peaker = request.user
            except Exception:
                pass
            existing = StepEntry.objects.filter(peaker=entry.peaker, date=entry.date).first()
            if existing:
                return HttpResponseRedirect(f"/steps/overwrite?date={form.cleaned_data['date']}&steps={form.cleaned_data['steps']}")
            request.session['last_activity'] = request.POST['activity']

            entry.save()
            
            return HttpResponseRedirect('/steps/?submitted=True')
    else:
        form = StepEntryForm(initial={'date': datetime.date.today})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'steps/steps.html', {
        'form': form, 'submitted': submitted, 'peaker': request.user, 'recent_steps': recent_steps, 'last_activity': activity, 'phase':settings.CURRENT_PHASE
        })

@login_required(login_url=reverse_lazy('login'))
def large_entry(request):
    submitted = False
    if request.method == 'POST':
        form = StepEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            try:
                entry.peaker = request.user
            except Exception:
                pass
            existing = StepEntry.objects.filter(peaker=entry.peaker, date=entry.date).first()
            if existing:
                return HttpResponseRedirect(f"/steps/overwrite?date={form.cleaned_data['date']}&steps={form.cleaned_data['steps']}")
            entry.save()
            return HttpResponseRedirect('/steps/?submitted=True')
    else:
        form = StepEntryForm(initial={'date': request.GET['date'], 'steps': request.GET['steps']})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'steps/large_entry.html', {'form': form, 'submitted': submitted, 'peaker': request.user,
                                                      'step_count_warning': _("You entered {form_steps_value} steps, which is a <b>LOT</b>!") % {'form_steps_value': form.steps.value})

@login_required(login_url=reverse_lazy('login'))    
def peaker_modification(request):
    submitted = False
    if request.method == 'POST':
        form = PeakerModificationForm(request.POST)
        if form.is_valid():
            original_group = request.user.profile.group
            original_team = request.user.profile.team
            entry = form.save(commit=False)
            try:
                # print(model_to_dict(entry))
                entry.peaker = request.user
                # TEMPORARY: The Group field is disabled, so make sure
                # it doesn't accidentally change here.
                entry.group = original_group
                entry.team = original_team
                # print(model_to_dict(entry))

                # TODO BUG This should only change team when the group has been changed.
                if entry.group and entry.group.team:
                    entry.team = entry.group.team
                if not request.user.profile.team and not entry.team:
                    # We need to calculate what team to put this peaker on.
                    counter = {}
                    for team in Team.objects.filter(auxiliary=False):
                        counter[team] = User.objects.filter(profile__team=team).count()
                    entry.team = min(counter, key=counter.get)
            except Exception as e:
                print(e)
            #print(model_to_dict(entry))
            entry.save()
            return HttpResponseRedirect('/peaker/?submitted=True')
    else:
        form = PeakerModificationForm(current_group=request.user.profile.group.pk if request.user.profile.group else None, initial={'group': request.user.profile.group, 'imperial': request.user.profile.imperial})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'steps/peaker.html', {'form': form, 'submitted': submitted, 'peaker': request.user})

@login_required(login_url=reverse_lazy('login'))
def step_report(request, peaker_name=''):
    unit_name = 'Kilometers'
    conv = 0.7242 / 1000.0
    # Units depends on the VIEWER, not the peaker whose steps we want
    if request.user.profile.imperial:
        unit_name = 'Miles'
        conv = 0.45 / 1000.0
    step_data = []
    step_total = 0
    distance_total = 0.0
    if peaker_name:
        peaker_name = urllib.parse.unquote(peaker_name)
        peaker = User.objects.get(username=peaker_name)
    else:
        peaker_name = 'you'
        peaker = request.user
    for entry in StepEntry.objects.filter(peaker=peaker).all().order_by('date'):
        distance = entry.steps * conv
        step_total += entry.steps
        distance_total += distance
        step_data.append({'day': entry.date, 'steps': entry.steps, 'distance': distance})
    step_data.append({'day': 'Total', 'steps': step_total, 'distance': distance_total})
    return render(request, 'steps/report.html', {'unit_name': unit_name, 'steps': step_data, 'peaker_name': peaker_name, 'phase': settings.CURRENT_PHASE})

@login_required(login_url=reverse_lazy('login'))
def overwrite_confirm(request):
    submitted = False
    existing = None
    sum_steps = 0
    if request.method == 'POST':
        form = StepEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            try:
                entry.peaker = request.user
            except Exception:
                pass
            existing = StepEntry.objects.filter(peaker=entry.peaker, date=entry.date).first()
            if existing:
                existing.delete()
            entry.save()
            return HttpResponseRedirect('/steps/?submitted=True')
    else:
        existing = StepEntry.objects.filter(peaker=request.user, date=request.GET['date']).first()
        form = StepEntryForm(initial={'date': request.GET['date'], 'steps': request.GET['steps']})
        sum_steps = existing.steps + int(request.GET['steps'])
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'steps/overwrite.html', {'form': form, 'submitted': submitted, 'peaker': request.user, 'existing': existing, 'sum_steps': sum_steps,
                                                    'dupliate_step_warning': _("On {date_entered} you entered {steps} steps for {date}. Do you want to change it to {new_steps} steps, or are these additional steps?" % {'date_entered': existing.entered, 'steps':existing.steps, 'date': existing.date, 'new_steps': form.steps.value}),
                                                    'overwrite_button': _("Overwrite with {new_steps}") % {'new_steps': form.steps.value}})

class StepData:
    def __init__(self, step_data, peaker_sets, unit_name, conversion, empty_key_name='---'):
        self.unit_name = unit_name
        self.data = []
        self.total_peakers = 0
        self.total_steps = 0
        self.total_distance = 0.0
        for key in sorted(step_data.keys(), key=lambda x: x.name if x else empty_key_name):
            self.data.append({'key': key.name if key else empty_key_name,
                              'steps': step_data[key],
                              'distance': step_data[key] * conversion,
                              'num_peakers': len(peaker_sets[key])})
            self.total_peakers += len(peaker_sets[key])
            self.total_steps += step_data[key]
        self.total_distance = self.total_steps * conversion

        
@staff_member_required
def admin_report(request):
    #never_logged_in_users = User.objects.filter(last_login=None).order_by('profile__group__name')
    #never_logged_steps = User.objects.exclude(pk__in=StepEntry.objects.values_list('peaker')).exclude(pk__in=never_logged_in_users).order_by('profile__group__name')
    unit_name = 'Kilometers'
    conv = 0.7242 / 1000.0
    if request.user.profile.imperial:
        unit_name = 'Miles'
        conv = 0.45 / 1000.0
    team_step_data = defaultdict(int)
    team_peakers = defaultdict(set)
    group_step_data = {}
    group_peakers = {}
    peaker_cache = {}
    for entry in StepEntry.objects.values('peaker', 'steps'):
        profile = peaker_cache.get(entry['peaker'], None)
        if not profile:
            peaker_cache[entry['peaker']] = Profile.objects.get(pk=entry['peaker'])
            profile = peaker_cache.get(entry['peaker'])
        team = profile.team
        group = profile.group
        team_step_data[team] += entry['steps']
        team_peakers[team].add(entry['peaker'])
        if team not in group_step_data:
            group_step_data[team] = defaultdict(int)
            group_peakers[team] = defaultdict(set)
        group_step_data[team][group] += entry['steps']
        group_peakers[team][group].add(entry['peaker'])
    # Create separate group StepDatas for each team
    group_step_data_objects = [(t.name, StepData(group_step_data[t], group_peakers[t], unit_name, conv, 'Peakers United')) for t in group_step_data]

    return render(request, 'steps/admin_report.html', {'team_data': StepData(team_step_data, team_peakers, unit_name, conv), 'group_data': group_step_data_objects})
