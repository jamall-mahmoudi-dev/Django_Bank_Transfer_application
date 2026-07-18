from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'phone_number', 'card_number', 'balance',
        'is_staff', 'is_active',
    )
    search_fields = ('username', 'phone_number', 'national_code', 'card_number', 'email')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('اطلاعات بانکی', {'fields': ('phone_number', 'national_code', 'card_number', 'balance')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('اطلاعات بانکی', {'fields': ('phone_number', 'national_code', 'card_number')}),
    )
