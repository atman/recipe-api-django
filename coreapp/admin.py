from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from coreapp import models


class CustomUserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'last_login']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Activity'), {'fields':('last_login', 'created_on')})
    )
    # Go through Admin model documentation to understand this better
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Tag)


