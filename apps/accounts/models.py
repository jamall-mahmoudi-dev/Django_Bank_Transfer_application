from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)  # اضافه شود
    card_number = models.CharField(max_length=16, blank=True, null=True)  # اضافه شود
    
    class Meta:
        app_label = 'accounts'
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} - {self.phone_number}"