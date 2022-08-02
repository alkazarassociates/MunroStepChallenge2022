from django.shortcuts import render
from .models import Team

def index(request):
    context = {'team_list': Team.objects.order_by('name')}
    return render(request, 'teams/teams.html', context)
