from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    balance = models.DecimalField(
        max_digits=15, 
        decimal_places=0, 
        default=0,
        verbose_name='موجودی (ریال)'
    )  
    
    class Meta:
        app_label = 'accounts'
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} - {self.phone_number}"

    @property
    def bank_balance(self):
        """موجودی واقعی از BankAccount (اپ bank) که با انتقال‌های واقعی
        به‌روز می‌شود. فیلد balance بالا دیگر توسط اپ transactions همگام
        نمی‌شود - در تمپلیت‌ها و ویوها به‌جای user.balance از همین استفاده کنید."""
        account = getattr(self, 'bank_account', None)
        return account.balance if account else 0