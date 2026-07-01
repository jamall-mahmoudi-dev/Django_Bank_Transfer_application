from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('transactions:new'), name='home'),
    path('accounts/', include('apps.accounts.urls')),
    path('transactions/', include('apps.transactions.urls')),
]