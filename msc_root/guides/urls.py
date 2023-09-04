from django.urls import path
from . import views

urlpatterns = [
    path('mpc_munro', views.MpcMunroGuide, name='mpc_guide'),
    path('', views.index, name='index'),
]