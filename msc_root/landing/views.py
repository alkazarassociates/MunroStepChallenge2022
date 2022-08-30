from django.shortcuts import render
from django.db.models import Sum
from steps.models import StepEntry

def index(request):
    total = 0
    if request.user.is_authenticated:
        total = StepEntry.objects.filter(peaker=request.user).aggregate(Sum('steps'))['steps__sum']
    return render(request, 'landing/landing.html', {'total_steps': total})
