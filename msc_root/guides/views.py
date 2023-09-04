from django.conf import settings
from django.shortcuts import render

def MpcMunroGuide(request):
    return render(request, 'guides/mpc_munro_guide.html', {'phase': settings.CURRENT_PHASE})