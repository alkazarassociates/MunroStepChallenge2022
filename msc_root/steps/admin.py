from django.contrib import admin

from .models import Profile, StepEntry

class StepEntryAdmin(admin.ModelAdmin):
    list_display = ('peaker', 'entered', 'date', 'steps', 'valid', 'notes')
    list_filter = ('entered', 'date', 'peaker')
    readonly_fields = ('entered',)

admin.site.register(StepEntry, StepEntryAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('peaker', 'get_email', 'get_active', 'group', 'team')
    list_filter = ('group', 'team')
    search_fields = ('peaker__username', 'peaker__email')

    def get_email(self, obj):
        return obj.peaker.email
    get_email.short_description = 'Email'
    
    def get_active(self, obj):
        return obj.peaker.is_active
    get_active.short_description = 'Active'

admin.site.register(Profile, ProfileAdmin)