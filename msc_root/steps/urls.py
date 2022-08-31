from django.urls import path

from . import views

urlpatterns = [
    path('large_entry', views.large_entry, name='large_entry'),
    path('overwrite', views.overwrite_confirm, name='overwrite_confirm'),
    path('report', views.step_report, name='step_report'),
    path('', views.step_entry, name='step_entry'),
]