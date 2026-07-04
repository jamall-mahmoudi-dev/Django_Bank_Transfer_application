from django.db import models
from django.conf import settings

class BankAccount(models.Model):
    """حساب بانکی فیک برای تست ب"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bank_account')
    card_number = models.CharField(max_length=16, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.card_number} - {self.balance:,} ریال"


class BankTransaction(models.Model):
    """تراکنش‌های بانکی فیک"""
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('success', 'موفق'),
        ('failed', 'ناموفق'),
    ]
    
    tracking_code = models.CharField(max_length=50, unique=True)
    source_card = models.CharField(max_length=16)
    destination_card = models.CharField(max_length=16)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    fee = models.DecimalField(max_digits=15, decimal_places=0, default=5000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reference_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.tracking_code} - {self.amount:,} ریال"