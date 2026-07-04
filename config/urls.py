from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('transactions:new'), name='home'),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.dashboard.urls')),
    path('home/', lambda request: redirect('/'), name='home'), 
    path('bank/', include('apps.bank.urls')),
    path('transactions/', include('apps.transactions.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)