from django.urls import path

from . import views

urlpatterns = [
    path('large_entry', views.large_entry, name='large_entry'),
    path('', views.step_entry, name='step_entry'),
]