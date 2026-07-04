from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import TransferForm
from .models import Transaction
import uuid

@login_required
def transfer_money(request):
    # بررسی وجود کارت مبدأ برای کاربر
    if not request.user.card_number:
        messages.error(request, 'لطفاً ابتدا شماره کارت خود را در پروفایل ثبت کنید')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            destination_card = form.cleaned_data['destination_card']
            amount = form.cleaned_data['amount']
            
            # بررسی اینکه کارت مقصد با کارت مبدأ یکی نباشد
            if destination_card == request.user.card_number:
                messages.error(request, 'شماره کارت مقصد نمی‌تواند با کارت مبدأ یکی باشد')
                return render(request, 'transactions/transfer.html', {'form': form})
            
            # محاسبه مبلغ کل با کارمزد
            fee = 5000
            total_amount = amount + fee
            
            # بررسی موجودی کاربر (از مدل User)
            if request.user.balance < total_amount:
                messages.error(request, f'موجودی کافی نیست. موجودی: {request.user.balance:,} ریال')
                return render(request, 'transactions/transfer.html', {'form': form})
            
            # ایجاد کد پیگیری
            tracking_code = str(uuid.uuid4()).replace('-', '')[:20]
            
            # ایجاد تراکنش
            transaction = Transaction.objects.create(
                user=request.user,
                tracking_code=tracking_code,
                source_card=request.user.card_number,
                destination_card=destination_card,
                amount=amount,
                fee=fee,
                status='success'  # برای تست مستقیم موفق در نظر گرفته می‌شود
            )
            
            # کم کردن از موجودی کاربر
            request.user.balance -= total_amount
            request.user.save()
            
            messages.success(request, f'انتقال با موفقیت انجام شد. کد پیگیری: {tracking_code}')
            return redirect('transactions:success', tracking_code=tracking_code)
        else:
            # اگر فرم خطا داشت
            messages.error(request, 'لطفاً اطلاعات را به درستی وارد کنید')
    else:
        form = TransferForm()
    
    return render(request, 'transactions/transfer.html', {'form': form})


@login_required
def transaction_success(request, tracking_code):
    transaction = get_object_or_404(Transaction, tracking_code=tracking_code, user=request.user)
    return render(request, 'transactions/success.html', {'transaction': transaction})


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)[:50]
    return render(request, 'transactions/history.html', {'transactions': transactions})


@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    return render(request, 'transactions/detail.html', {'transaction': transaction})