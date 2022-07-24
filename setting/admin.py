from django.contrib import admin
from .models import *

# Register your models here.


class SettingAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=...):
        return False

    list_display = [
        'terms',
        'edit'
    ]
    list_display_links = ['edit']
    list_editable = [
        'terms',
    ]


admin.site.register(Setting, SettingAdmin)
