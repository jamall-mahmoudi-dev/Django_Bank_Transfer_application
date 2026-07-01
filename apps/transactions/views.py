from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import TransferForm
from .models import Transaction
from .bank_api import BankAPI
import uuid

@login_required
def transfer_money(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            destination_card = form.cleaned_data['destination_card']
            amount = form.cleaned_data['amount']
            
            # بررسی وجود کارت مبدأ برای کاربر
            if not request.user.card_number:
                messages.error(request, 'لطفاً ابتدا شماره کارت خود را در پروفایل ثبت کنید')
                return redirect('accounts:profile')
            
            # بررسی موجودی از طریق API بانک
            bank_api = BankAPI()
            balance_check = bank_api.check_balance(request.user.card_number)
            
            if not balance_check['success']:
                messages.error(request, balance_check.get('error', 'خطا در بررسی موجودی'))
                return redirect('transactions:new')
            
            total_amount = amount + 5000  # 5000 ریال کارمزد
            
            if balance_check['balance'] < total_amount:
                messages.error(request, f'موجودی کافی نیست. موجودی: {balance_check["balance"]:,} ریال')
                return redirect('transactions:new')
            
            # ایجاد تراکنش
            tracking_code = str(uuid.uuid4()).replace('-', '')[:20]
            
            transaction = Transaction.objects.create(
                user=request.user,
                tracking_code=tracking_code,
                source_card=request.user.card_number,
                destination_card=destination_card,
                amount=amount,
                fee=5000,
                status='pending'
            )
            
            # انجام انتقال در بانک
            result = bank_api.transfer(
                source_card=request.user.card_number,
                destination_card=destination_card,
                amount=amount,
                tracking_code=tracking_code
            )
            
            if result['success']:
                transaction.status = 'success'
                transaction.bank_reference = result['reference_id']
                transaction.save()
                
                # بروزرسانی موجودی کاربر (در سیستم خودمان)
                request.user.balance -= total_amount
                request.user.save()
                
                messages.success(request, f'انتقال با موفقیت انجام شد. کد پیگیری: {tracking_code}')
                return redirect('transactions:success', tracking_code=tracking_code)
            else:
                transaction.status = 'failed'
                transaction.save()
                messages.error(request, f'خطا در انجام تراکنش: {result["error"]}')
                return redirect('transactions:new')
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