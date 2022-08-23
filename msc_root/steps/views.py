from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.models import User

import datetime

from .models import Profile, StepEntry
from .forms import PeakerRegistrationForm, StepEntryForm
from mpc_groups.models import MpcGroup

class Register(CreateView):
            
    template_name: str = 'registration/register.html'
    form_class = PeakerRegistrationForm
    success_url = reverse_lazy('register-success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MPC_GROUPS'] = MpcGroup.objects.order_by('name')
        return context

    def form_valid(self, form):
        form.save()
        # Now save the profile
        prof = Profile.objects.get(peaker=User.objects.get(username=form.cleaned_data['username']))
        prof.group=form.cleaned_data['group_field']
        prof.save()
        return HttpResponseRedirect(self.success_url)

@login_required(login_url=reverse_lazy('login'))
def step_entry(request):
    submitted = False
    if request.method == 'POST':
        form = StepEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            try:
                entry.peaker = request.user
            except Exception:
                pass
            entry.save()
            return HttpResponseRedirect('/steps/?submitted=True')
    else:
        form = StepEntryForm(initial={'date': datetime.date.today})
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'steps/steps.html', {'form': form, 'submitted': submitted, 'peaker': request.user})
