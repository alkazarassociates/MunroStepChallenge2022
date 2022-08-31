from django.shortcuts import render
from mpc_groups.models import MpcGroup
from .models import Team

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
    context = {'team': team, 'group_list': group_lines}
    return render(request, 'teams/team_page.html', context )
