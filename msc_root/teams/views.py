from django.shortcuts import render
from .models import Team

def index(request):
    context = {'team_list': Team.objects.order_by('name'), 'title': 'Munro Step Challenge'}
    return render(request, 'teams/teams.html', context)

def team_page(request, args):
    context = {'team': Team.objects.get(name=args)}
    return render(request, 'teams/team_page.html', context )
