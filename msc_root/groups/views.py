from django.shortcuts import render
from .models import Group

def index(request):
    context = {'group_list': Group.objects.order_by('name')}
    return render(request, 'groups/groups.html', context)

