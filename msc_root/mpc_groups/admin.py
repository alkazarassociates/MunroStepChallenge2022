from django.contrib import admin
from .models import MpcAdminRegistration, MpcGroup, GroupModifications

# Register your models here.
admin.site.register(MpcGroup)
admin.site.register(MpcAdminRegistration)
admin.site.register(GroupModifications)