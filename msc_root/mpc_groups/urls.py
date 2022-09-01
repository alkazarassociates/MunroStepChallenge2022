from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('register/', views.register),
    re_path(r'^(?P<group>[\w\&\,/ -]+)/members$', views.members, name='group_members'),
    path('', views.index, name='groups')
]