from django.urls import path, re_path
from . import views

urlpatterns = [
    path('register/', views.register, name='group_register'),
    re_path(r'^(?P<group>[\w\&\,/ -]+)/members$', views.members, name='group_members'),
    re_path(r'^(?P<group>[\w\&\,/ -]+)$', views.report, name='group_report'),
    path('', views.index, name='groups')
]