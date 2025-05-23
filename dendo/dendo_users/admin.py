from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_per_page = 20

    fieldsets = (
        ('User Info', {'fields': ('username', 'email', 'password', 'avatar', 'banner', 'is_verified')}),
        ('Important Info', {'fields':('last_login', 'date_joined', 'updated_at')}),
        ('Permissions', {'fields':('is_staff', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        ('About User',{
            'classes': ('wide',),
            'fields':(
                'username',
                'email',
                'password1',
                'password2',
                'is_verified',
                'is_staff',
                'is_active',
                'is_superuser'
            )
        }),
    )

    list_display = ['username', 'email', 'is_active', 'is_staff',]

    list_filter = ['date_joined', 'is_active', 'is_superuser', 'is_staff']

    readonly_fields = ['date_joined', 'updated_at', 'last_login']

    search_fields = ['username', 'email']

    ordering = ['username', 'last_login']

admin.site.register(CustomUser, CustomUserAdmin)