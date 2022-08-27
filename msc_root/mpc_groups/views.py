from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import MpcAdminRegistrationForm
from .models import GroupModifications, MpcGroup

def index(request):
    group_list = [ {'name': g.name, 'count': User.objects.filter(profile__group=g).count() } for g in MpcGroup.objects.order_by('name')]
    context = {
        'group_list': group_list,
        'no_group_count': User.objects.filter(profile__group=None).count,
        'total_peakers': User.objects.count,
        'updated': GroupModifications.objects.latest('modification_time').modification_time.strftime("%m/%d/%Y %H:%M"),
    }
    return render(request, 'mpc_groups/mpc_groups.html', context)

@login_required(login_url=reverse_lazy('login'))
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

