from django.shortcuts import render
from .models import MpcGroup

def index(request):
    context = {'group_list': MpcGroup.objects.order_by('name')}
    return render(request, 'mpc_groups/mpc_groups.html', context)

