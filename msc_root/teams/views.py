from django.db.models import Sum
from django.shortcuts import render
from mpc_groups.models import MpcGroup
from django.contrib.auth.models import User
from .models import Team
from steps.models import StepEntry

def index(request):
    context = {'team_list': Team.objects.order_by('name'), 'title': 'Munro Step Challenge'}
    return render(request, 'teams/teams.html', context)

def team_page(request, args):
    team = Team.objects.get(name=args)
    group_list = MpcGroup.objects.filter(team=team).order_by('name')
    groups = [group.name for group in group_list]
    while len(groups) % 3 != 0:
        groups.append('')
    group_lines = []
    for i in range(len(groups) // 3):
        group_lines.append([groups[3*i], groups[3*i+1], groups[3*i+2]])
    team_steps = StepEntry.objects.filter(peaker__profile__team=team).aggregate(Sum('steps'))['steps__sum']
    if team_steps is None:
        team_steps = 0
    context = {
        'team': team, 'group_list': group_lines, 'team_size': User.objects.filter(profile__team=team).count(), 
        'team_steps': team_steps}
    return render(request, 'teams/team_page.html', context )
