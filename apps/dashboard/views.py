from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.transactions.models import Transaction
from apps.accounts.models import User

@login_required
def dashboard(request):
    # دریافت تراکنش‌های کاربر
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # آمار کلی
    total_transactions = Transaction.objects.filter(user=request.user).count()
    total_amount = Transaction.objects.filter(user=request.user, status='success').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_fees = Transaction.objects.filter(user=request.user, status='success').aggregate(
        total=Sum('fee')
    )['total'] or 0
    
    # تعداد تراکنش‌های موفق و ناموفق
    success_count = Transaction.objects.filter(user=request.user, status='success').count()
    failed_count = Transaction.objects.filter(user=request.user, status='failed').count()
    pending_count = Transaction.objects.filter(user=request.user, status='pending').count()
    
    context = {
        'transactions': transactions,
        'total_transactions': total_transactions,
        'total_amount': total_amount,
        'total_fees': total_fees,
        'success_count': success_count,
        'failed_count': failed_count,
        'pending_count': pending_count,
        'user': request.user,
    }
    
    return render(request, 'dashboard/dashboard.html', context)