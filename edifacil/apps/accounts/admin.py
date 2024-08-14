from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from accounts.models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    model = User
    add_form_template = None
    search_fields = ['email']
    list_filter = ['is_staff', 'is_superuser']
    list_display = ['email']
    list_display_links = ['email']
    readonly_fields = ['date_joined', 'last_login']
    ordering = ['email']
    fieldsets = (
        (
            'Informações de login',
            {
                'fields': (
                    'email',
                    'password',
                )
            },
        ),
        (
            'Permissões',
            {
                'fields': (
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
        (
            'Datas importantes',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            },
        ),
    )
    add_fieldsets = (
        (
            'Informações de login',
            {
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
