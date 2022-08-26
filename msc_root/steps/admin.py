from django.contrib import admin

from .models import Profile, StepEntry

class StepEntryAdmin(admin.ModelAdmin):
    list_display = ('peaker', 'entered', 'date', 'steps', 'valid', 'notes')
    list_filter = ('entered', 'date', 'peaker')
    readonly_fields = ('entered',)

admin.site.register(StepEntry, StepEntryAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('peaker', 'group')
    search_fields = ('peaker__username',)

admin.site.register(Profile, ProfileAdmin)