from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from steps.models import StepEntry, Profile
from teams.models import Team
from .forms import MpcAdminRegistrationForm
from .models import GroupModifications, MpcGroup

def index(request):
    group_list = [ {'name': g.name, 'count': User.objects.filter(profile__group=g).count(), 'team': g.team } for g in MpcGroup.objects.order_by('name')]
    try:
        updateds = GroupModifications.objects.latest('modification_time').modification_time.strftime("%m/%d/%Y %H:%M")
    except:
        updateds = []

    context = {
        'group_list': group_list,
        'no_group_count': User.objects.filter(profile__group=None).count,
        'total_peakers': User.objects.count,
        'updated': updateds,
        'phase': settings.CURRENT_PHASE,
    }
    return render(request, 'mpc_groups/mpc_groups.html', context)

def register(request):
    # TODO 2023   Record username, make them in Group MPCAdmin
    submitted = False
    if request.method == 'POST':
        form = MpcAdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/groups/register/?submitted=True')
    else:
        form = MpcAdminRegistrationForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'mpc_groups/register.html', {'form': form, 'submitted': submitted, 'our_email':settings.EMAIL_OUR_ADDRESS, 'phase': settings.CURRENT_PHASE})

@login_required(login_url=reverse_lazy('login'))
def members(request, group):
    try:
        if group == 'Peakers United':
            g = None
        else:
            g = MpcGroup.objects.get(name=group)
    except MpcGroup.DoesNotExist:
        raise Http404("No Such Group")
    context = {'group': g, 'phasae': settings.CURRENT_PHASE, 'peakers': User.objects.filter(profile__group=g).order_by('username')}
    # Perhaps this could be an annotation, but I don't know how yet.
    for p in context['peakers']:
        p.has_steps = StepEntry.objects.filter(peaker=p).exists()
    return render(request, 'mpc_groups/members.html', context)

@login_required(login_url=reverse_lazy('login'))
def report(request, group):
    try:
        if isinstance(group, list):
            g = 'Custom Group'
        elif group=='Peakers United':
            g = None
        else:
            g = MpcGroup.objects.get(name=group)
    except MpcGroup.DoesNotExist:
        raise Http404("No Such Group")
    dates = StepEntry.objects.distinct('date').values_list('date')
    day_totals = []
    step_total = 0
    munro_step_total = 0  # Total steps of peakers who did not opt out.
    distance_total = 0
    unit_name = 'Kilometers'
    conv = 0.7242 / 1000.0
    if hasattr(request.user, 'profile') and request.user.profile.imperial:
        unit_name = 'Miles'
        conv = 0.45 / 1000.0
    for date in dates:
        day = date[0]
        if isinstance(group, list):
            entries = StepEntry.objects.filter(date=day, peaker__username__in=group)
        else:
            entries = StepEntry.objects.filter(date=day, peaker__profile__group=g)
            # justgiving==True means you have a personal page and do NOT want to count in
            # the group total.
            munro_entries = entries.filter(peaker__profile__justgiving=False)
        steps = entries.aggregate(Sum('steps'))['steps__sum'] or 0
        step_total += steps
        munro_step_total += munro_entries.aggregate(Sum('steps'))['steps__sum'] or 0
        distance = conv * steps
        distance_total += distance
        day_totals.append({'day': day, 'steps': steps, 'distance': distance})
    day_totals.append({'day': 'Total', 'steps': step_total, 'distance': distance_total})
    day_totals.append({'day': 'Total for JustGiving', 'steps': munro_step_total, 'distance': ''})

    if isinstance(group, list):
        entries = StepEntry.objects.filter(peaker__username__in=group)
    else:
        entries = StepEntry.objects.filter(peaker__profile__group=g)
    peakers = entries.distinct('peaker').values_list('peaker', 'peaker__username', 'peaker__profile__team')
    peaker_totals = []
    step_total = 0
    for peaker_wrap in peakers:
        if peaker_wrap[1] == 'admin':
            continue
        if peaker_wrap[2] is None:
            continue
        peaker = peaker_wrap[0]
        steps = StepEntry.objects.filter(peaker=peaker).aggregate(Sum('steps'))['steps__sum'] or 0
        step_total += steps
        team = None if g else Team.objects.get(pk=peaker_wrap[2])
        peaker_totals.append({'peaker': peaker_wrap[1], 'steps': steps, 'team': team})
    # Sort these alphabetically or by total.
    sort_by = request.GET.get('sort', 'Alpha') 
    if  sort_by == 'Steps':
        peaker_totals.sort(key=lambda t: t['steps'], reverse=True)
    elif sort_by == 'Team':
        peaker_totals.sort(key=lambda t: t['team'].name)
    else:
        peaker_totals.sort(key=lambda t: t['peaker'].lower())

    peaker_totals.append({'peaker': 'Total', 'steps': step_total})
    context = {'group': g or 'Peakers United', 'unit_name': unit_name, 'day_totals': day_totals, 'peaker_totals': peaker_totals, 'sort': request.GET.get('sort', 'Alpha'),
        'show_teams': (g is None), 'phase': settings.CURRENT_PHASE,
    }
    return render(request, 'mpc_groups/report.html', context)

def pseudo_group_report(request):
    return report(request, request.GET.getlist('members[]'))
