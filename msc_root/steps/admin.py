from django.contrib import admin

from .models import StepEntry

class StepEntryAdmin(admin.ModelAdmin):
    list_display = ('peaker', 'entered', 'date', 'activity', 'amount', 'valid')
    list_filter = ('entered', 'date', 'peaker')
    readonly_fields = ('entered',)

admin.site.register(StepEntry, StepEntryAdmin)
