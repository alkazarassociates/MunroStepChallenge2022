from django.contrib import admin
from .models import MpcAdminRegistration, MpcGroup

# Register your models here.
admin.site.register(MpcGroup)
admin.site.register(MpcAdminRegistration)