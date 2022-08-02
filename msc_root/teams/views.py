from django.shortcuts import render
from .models import Team

def index(request):
    context = {'team_list': Team.objects.order_by('name'), 'title': 'Munro Step Challenge Teams'}
    return render(request, 'teams/teams.html', context)
