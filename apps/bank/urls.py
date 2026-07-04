from django.urls import path
from . import views

app_name = 'bank'

urlpatterns = [
    path('test/', views.test_bank_api, name='test_api'),
    path('api/check-balance/', views.api_check_balance, name='api_check_balance'),
    path('api/transfer/', views.api_transfer, name='api_transfer'),
    path('api/create-account/', views.api_create_account, name='api_create_account'),
]