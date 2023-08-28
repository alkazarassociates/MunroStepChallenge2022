from django.contrib import admin
from .models import MpcAdminRegistration, MpcGroup, GroupModifications

# Register your models here.
class MpcGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'admin')

admin.site.register(MpcGroup, MpcGroupAdmin)
admin.site.register(MpcAdminRegistration)
admin.site.register(GroupModifications)