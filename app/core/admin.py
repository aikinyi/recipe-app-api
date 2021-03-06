from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Tag, Ingredient


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Registering
    """
    search_fields = ['id', 'name', 'email']
    list_display = ['id', 'name', 'email']
    ordering = ['id']
    fieldsets = (
        (None, {
            "fields": (
                'email', 'password'
            ),
        }),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active','is_staff','is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Tag)
class Tag(admin.ModelAdmin):
    search_fields = ['__all__']


@admin.register(Ingredient)
class Ingredient(admin.ModelAdmin):
    search_fields = ['__all__']