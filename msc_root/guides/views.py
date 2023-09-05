from django.conf import settings
from django.shortcuts import render
from .movie_list import MOVIE_LIST
from .show_list import SHOW_LIST
from teams.models import Team


def MpcMunroGuide(request):
    return render(request, 'guides/mpc_munro_guide.html', {'phase': settings.CURRENT_PHASE})

def index(request):
    return render(request, 'guides/index.html', {'phase': settings.CURRENT_PHASE})

def movies(request):
    return render(request, 'guides/list.html', {'phase': settings.CURRENT_PHASE, 'title': 'Movies to Inspire', 'list_items': MOVIE_LIST})

def shows(request):
    return render(request, 'guides/list.html', {'phase': settings.CURRENT_PHASE, 'title': 'TV Shows to Inspire', 'list_items': SHOW_LIST})

def team_notes(request):
    context = {'team_list': Team.objects.order_by('name'), 'title': 'Our Hidden Figures', 'phase': settings.CURRENT_PHASE}
    return render(request, 'guides/team_notes.html', context)