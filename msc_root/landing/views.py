from django.conf import settings
from django.shortcuts import render
from django.db.models import Sum
from steps.models import StepEntry

def index(request):
    total = 0
    if request.user.is_authenticated:
        total = StepEntry.objects.filter(peaker=request.user).aggregate(Sum('steps'))['steps__sum']
        if total is None:
            total = 0
    return render(request, 'landing/landing.html', {'total_steps': total, 'phase': settings.CURRENT_PHASE})
