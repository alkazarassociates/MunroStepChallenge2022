from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from steps.models import StepEntry
from .forms import MpcAdminRegistrationForm
from .models import GroupModifications, MpcGroup

def index(request):
    group_list = [ {'name': g.name, 'count': User.objects.filter(profile__group=g).count(), 'team': g.team } for g in MpcGroup.objects.order_by('name')]
    context = {
        'group_list': group_list,
        'no_group_count': User.objects.filter(profile__group=None).count,
        'total_peakers': User.objects.count,
        'updated': GroupModifications.objects.latest('modification_time').modification_time.strftime("%m/%d/%Y %H:%M"),
    }
    return render(request, 'mpc_groups/mpc_groups.html', context)

@login_required(login_url=reverse_lazy('login'))
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

    return render(request, 'mpc_groups/register.html', {'form': form, 'submitted': submitted})

@login_required(login_url=reverse_lazy('login'))
def members(request, group):
    try:
        g = MpcGroup.objects.get(name=group)
    except MpcGroup.DoesNotExist:
        raise Http404("No Such Group")
    context = {'group': g, 'peakers': User.objects.filter(profile__group=g).order_by('username')}
    return render(request, 'mpc_groups/members.html', context)

@login_required(login_url=reverse_lazy('login'))
def report(request, group):
    try:
        g = MpcGroup.objects.get(name=group)
    except MpcGroup.DoesNotExist:
        raise Http404("No Such Group")
    dates = StepEntry.objects.distinct('date').values_list('date')
    day_totals = []
    step_total = 0
    mile_total = 0
    for date in dates:
        day = date[0]
        steps = StepEntry.objects.filter(date=day, peaker__profile__group=g).aggregate(Sum('steps'))['steps__sum'] or 0
        step_total += steps
        miles = 0.45 * steps / 1000.0
        mile_total += miles
        day_totals.append({'day': day, 'steps': steps, 'miles': miles})
    day_totals.append({'day': 'Total', 'steps': step_total, 'miles': mile_total})

    peakers = StepEntry.objects.filter(peaker__profile__group=g).distinct('peaker').values_list('peaker', 'peaker__username')
    peaker_totals = []
    step_total = 0
    for peaker_wrap in peakers:
        peaker = peaker_wrap[0]
        steps = StepEntry.objects.filter(peaker=peaker).aggregate(Sum('steps'))['steps__sum'] or 0
        step_total += steps
        peaker_totals.append({'peaker': peaker_wrap[1], 'steps': steps})
    # Sort these alphabetically or by total.
    if request.GET.get('sorted', 'False') == 'True':
        peaker_totals.sort(key=lambda t: t['steps'], reverse=True)
    else:
        peaker_totals.sort(key=lambda t: t['peaker'].lower())

    peaker_totals.append({'peaker': 'Total', 'steps': step_total})
    context = {'group': g, 'day_totals': day_totals, 'peaker_totals': peaker_totals, 'sort': 'Top steps' if request.GET.get('sorted', False) else 'Alpha'}
    return render(request, 'mpc_groups/report.html', context)