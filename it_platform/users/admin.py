from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Кастомдукураган колдонуучу администратор панели
    """
    model = CustomUser
    list_display = [
        'email', 'username', 'first_name', 'last_name',
        'is_active', 'is_staff', 'date_joined'
    ]
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Жеке маалымат', {'fields': ('first_name', 'last_name')}),
        ('Уруксаттар', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Маанилүү даталар', {'fields': ('last_login', 'date_joined')}),
        ('Топтор', {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name',
                'password1', 'password2', 'is_active', 'is_staff'
            ),
        }),
    )
