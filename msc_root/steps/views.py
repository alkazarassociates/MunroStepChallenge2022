from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import StepEntry
from .forms import StepEntryForm

class Register(CreateView):
    template_name: str = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

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
