from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

card_number_validator = RegexValidator(
    regex=r'^\d{16}$',
    message='شماره کارت باید دقیقاً ۱۶ رقم باشد.'
)


class BankAccount(models.Model):
    """حساب بانکی فیک برای تست درگاه پرداخت.

    توجه: user اختیاری است چون کارت‌های مقصد استفاده‌شده در تست
    (مثل نمونه‌های ساخته‌شده در shell) لزوماً به یک کاربر ثبت‌نامی متصل نیستند.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bank_account',
        null=True,
        blank=True,
    )
    card_number = models.CharField(
        max_length=16,
        unique=True,
        validators=[card_number_validator],
    )
    balance = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.card_number} - {self.balance:,} ریال"


class BankTransaction(models.Model):
    """تراکنش‌های بانکی فیک."""
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('success', 'موفق'),
        ('failed', 'ناموفق'),
    ]

    tracking_code = models.CharField(max_length=50, unique=True)
    source_card = models.CharField(max_length=16, validators=[card_number_validator])
    destination_card = models.CharField(max_length=16, validators=[card_number_validator])
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    fee = models.DecimalField(max_digits=15, decimal_places=0, default=5000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reference_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tracking_code} - {self.amount:,} ریال"
