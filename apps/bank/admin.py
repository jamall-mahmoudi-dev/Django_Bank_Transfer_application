from django.contrib import admin

from .models import BankAccount, BankTransaction


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'user', 'balance', 'is_active', 'created_at')
    search_fields = ('card_number', 'user__username')
    list_filter = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'source_card', 'destination_card', 'amount', 'status', 'created_at')
    search_fields = ('tracking_code', 'source_card', 'destination_card', 'reference_id')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
