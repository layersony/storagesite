from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Unit, Booking

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'name', 'last_login')}),
        ('Permissions', {'fields': (
            'user_type',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username','email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'name', 'user_type', 'is_staff', 'is_active','last_login')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


