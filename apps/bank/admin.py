from django.contrib import admin
from .models import BankAccount, BankTransaction

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'balance', 'is_active', 'created_at')
    search_fields = ('card_number',)
    list_filter = ('is_active',)

@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'source_card', 'destination_card', 'amount', 'status', 'created_at')
    search_fields = ('tracking_code', 'source_card', 'destination_card')
    list_filter = ('status',)