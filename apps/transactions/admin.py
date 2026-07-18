from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'tracking_code', 'user', 'source_card', 'destination_card',
        'amount', 'status', 'created_at',
    )
    search_fields = ('tracking_code', 'source_card', 'destination_card', 'bank_reference')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
