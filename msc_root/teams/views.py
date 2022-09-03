from django.db.models import Sum
from django.shortcuts import render
from mpc_groups.models import MpcGroup
from django.contrib.auth.models import User
from .models import Team
from steps.models import StepEntry

def index(request):
    context = {'team_list': Team.objects.order_by('name'), 'title': 'Munro Step Challenge'}
    return render(request, 'teams/teams.html', context)

def nb(text):
    return text.replace(' ', "&nbsp;")

def amp(text):
    return text.replace(' & ', '&amp;')

def pp(text):
    return nb(amp(text))

def team_page(request, args):
    team = Team.objects.get(name=args)
    group_list = MpcGroup.objects.filter(team=team).order_by('name')
    groups = [pp(group.name) for group in group_list]
    while len(groups) % 3 != 0:
        groups.append('')
    group_lines = []
    for i in range(len(groups) // 3):
        group_lines.append([groups[3*i], groups[3*i+1], groups[3*i+2]])

    dates = StepEntry.objects.distinct('date').values_list('date')
    day_totals = []
    step_total = 0
    distance_total = 0
    unit_name = 'Kilometers'
    conv = 0.7242 / 1000.0
    if hasattr(request.user, 'profile') and request.user.profile.imperial:
        unit_name = 'Miles'
        conv = 0.45 / 1000.0
    for date in dates:
        day = date[0]
        steps = StepEntry.objects.filter(date=day, peaker__profile__team=team).aggregate(Sum('steps'))['steps__sum'] or 0
        step_total += steps
        distance = conv * steps
        distance_total += distance
        day_totals.append({'day': day, 'steps': steps, 'distance': distance})
    day_totals.append({'day': 'Total', 'steps': step_total, 'distance': distance_total})

    context = {
        'team': team, 'group_list': group_lines, 'team_size': User.objects.filter(profile__team=team).count(), 
        'team_steps': step_total, 'day_totals': day_totals, 'unit_name': unit_name}
    return render(request, 'teams/team_page.html', context )
