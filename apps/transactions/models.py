
from django.db import models
from django.conf import settings

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('success', 'موفق'),
        ('failed', 'ناموفق'),
        ('reversed', 'برگشت خورده'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    tracking_code = models.CharField(max_length=50, unique=True, verbose_name='کد پیگیری')
    source_card = models.CharField(max_length=16, verbose_name='کارت مبدأ')
    destination_card = models.CharField(max_length=16, verbose_name='کارت مقصد')
    amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='مبلغ (ریال)')
    fee = models.DecimalField(max_digits=15, decimal_places=0, default=5000, verbose_name='کارمزد (ریال)')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    bank_reference = models.CharField(max_length=100, blank=True, verbose_name='مرجع بانک')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.tracking_code} - {self.amount} ریال"