from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),  # not title
        ('Profile', {'fields': ('role', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')})
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),  # for form wider (bigger)
                'fields': ('email', 'username', 'password1', 'password2', 'role')}),
    )

    readonly_fields = ('created_at', 'updated_at')
