from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import StepEntry
from .forms import StepEntryForm

def step_entry(request):
    submitted = False
    if request.method == 'POST':
        form = StepEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/steps/?submitted=True')
    else:
        form = StepEntryForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'steps/steps.html', {'form': form, 'submitted': submitted})
