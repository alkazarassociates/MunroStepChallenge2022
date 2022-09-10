from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from collections import defaultdict
import datetime

from .models import Profile, StepEntry
from .forms import PeakerRegistrationForm, StepEntryForm, PeakerModificationForm
from mpc_groups.models import MpcGroup
from teams.models import Team

class Register(CreateView):
            
    template_name: str = 'registration/register.html'
    form_class = PeakerRegistrationForm
    success_url = reverse_lazy('register-success')

    # TODO 2023
    #  Consider email for password resets.
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


@login_required(login_url=reverse_lazy('login'))
def step_entry(request):
    submitted = False
    latest = None
    steps = StepEntry.objects.filter(peaker=request.user)
    if steps:
        latest = steps.latest('entered')
        d = latest.date.strftime("%B %d")
        recent_steps = str(latest.steps) + " steps for " + d
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
        'form': form, 'submitted': submitted, 'peaker': request.user, 'recent_steps': recent_steps, 'last_activity': activity
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

    return render(request, 'steps/large_entry.html', {'form': form, 'submitted': submitted, 'peaker': request.user})

@login_required(login_url=reverse_lazy('login'))    
def peaker_modification(request):
    submitted = False
    if request.method == 'POST':
        form = PeakerModificationForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            try:
                entry.peaker = request.user
                if entry.group and entry.group.team:
                    entry.team = entry.group.team
                if not entry.team:
                    # We need to calculate what team to put this peaker on.
                    counter = {}
                    for team in Team.objects.filter(auxiliary=False):
                        counter[team] = User.objects.filter(profile__team=team).count()
                    entry.team = min(counter, key=counter.get)
            except Exception:
                pass
            entry.save()
            return HttpResponseRedirect('/peaker/?submitted=True')
    else:
        form = PeakerModificationForm(current_group=request.user.profile.group.pk, initial={'group': request.user.profile.group, 'imperial': request.user.profile.imperial})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'steps/peaker.html', {'form': form, 'submitted': submitted, 'peaker': request.user})

@login_required(login_url=reverse_lazy('login'))
def step_report(request):
    unit_name = 'Kilometers'
    conv = 0.7242 / 1000.0
    if request.user.profile.imperial:
        unit_name = 'Miles'
        conv = 0.45 / 1000.0
    step_data = []
    step_total = 0
    distance_total = 0.0
    for entry in StepEntry.objects.filter(peaker=request.user).all().order_by('date'):
        distance = entry.steps * conv
        step_total += entry.steps
        distance_total += distance
        step_data.append({'day': entry.date, 'steps': entry.steps, 'distance': distance})
    step_data.append({'day': 'Total', 'steps': step_total, 'distance': distance_total})
    return render(request, 'steps/report.html', {'unit_name': unit_name, 'steps': step_data})

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

    return render(request, 'steps/overwrite.html', {'form': form, 'submitted': submitted, 'peaker': request.user, 'existing': existing, 'sum_steps': sum_steps})

class StepData:
    def __init__(self, step_data, unit_name, conversion, empty_key_name='---'):
        self.unit_name = unit_name
        self.data = []
        self.total_steps = 0
        self.total_distance = 0.0
        for key in sorted(step_data.keys(), key=lambda x: x.name if x else empty_key_name):
            self.data.append({'key': key.name if key else empty_key_name,
                              'steps': step_data[key],
                              'distance': step_data[key] * conversion})
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
    group_step_data = {}
    peaker_cache = {}
    for entry in StepEntry.objects.values('peaker', 'steps'):
        profile = peaker_cache.get(entry['peaker'], None)
        if not profile:
            peaker_cache[entry['peaker']] = Profile.objects.get(pk=entry['peaker'])
            profile = peaker_cache.get(entry['peaker'])
        team = profile.team
        group = profile.group
        team_step_data[team] += entry['steps']
        if team not in group_step_data:
            group_step_data[team] = defaultdict(int)
        group_step_data[team][group] += entry['steps']
    # Create separate group StepDatas for each team
    group_step_data_objects = [(t.name, StepData(group_step_data[t], unit_name, conv, 'Peakers United')) for t in group_step_data]

    return render(request, 'steps/admin_report.html', {'team_data': StepData(team_step_data, unit_name, conv), 'group_data': group_step_data_objects})
