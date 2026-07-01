from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('new/', views.transfer_money, name='new'),
    path('success/<str:tracking_code>/', views.transaction_success, name='success'),
    path('history/', views.transaction_history, name='history'),
    path('detail/<int:pk>/', views.transaction_detail, name='detail'),
]