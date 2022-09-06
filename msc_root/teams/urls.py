from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'(?P<team_name>\w+)', views.team_page, name='team_page'),
    path('', views.index, name='teams')
]