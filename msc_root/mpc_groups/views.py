from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import MpcAdminRegistrationForm
from .models import MpcGroup

def index(request):
    context = {'group_list': MpcGroup.objects.order_by('name')}
    return render(request, 'mpc_groups/mpc_groups.html', context)

def register(request):
    submitted = False
    if request.method == 'POST':
        form = MpcAdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/groups/register/?submitted=True')
    else:
        form = MpcAdminRegistrationForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'mpc_groups/register.html', {'form': form, 'submitted': submitted})

