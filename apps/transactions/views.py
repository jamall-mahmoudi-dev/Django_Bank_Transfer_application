import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TransferForm
from .models import Transaction

# این import را متناسب با مسیر واقعی اپ bank در پروژه‌تان تنظیم کنید
# (طبق apps/bank/apps.py فعلی، مسیر باید apps.bank باشد)
try:
    from apps.bank.api import BankAPI
except ImportError:
    from bank.api import BankAPI

bank_api = BankAPI()


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
            source_card = request.user.card_number

            if destination_card == source_card:
                messages.error(request, 'شماره کارت مقصد نمی‌تواند با کارت مبدأ یکی باشد')
                return render(request, 'transactions/transfer.html', {'form': form})

            tracking_code = str(uuid.uuid4()).replace('-', '')[:20]

            # انتقال واقعی از طریق درگاه بانک فیک (apps/bank). این تابع خودش
            # atomic است، موجودی هر دو کارت را در BankAccount چک/به‌روزرسانی
            # می‌کند و جلوی برداشت بدون واریز به مقصد را می‌گیرد.
            result = bank_api.transfer(
                source_card, destination_card, amount, tracking_code=tracking_code
            )

            # ثبت رکورد محلی تراکنش برای تاریخچه/نمایش به کاربر - چه موفق چه ناموفق
            Transaction.objects.create(
                user=request.user,
                tracking_code=tracking_code,
                source_card=source_card,
                destination_card=destination_card,
                amount=amount,
                fee=result.get('fee', 5000),
                status='success' if result['success'] else 'failed',
                bank_reference=result.get('reference_id', ''),
            )

            if not result['success']:
                messages.error(request, result['error'])
                return render(request, 'transactions/transfer.html', {'form': form})

            messages.success(request, f'انتقال با موفقیت انجام شد. کد پیگیری: {tracking_code}')
            return redirect('transactions:success', tracking_code=tracking_code)
        else:
            messages.error(request, 'لطفاً اطلاعات را به درستی وارد کنید')
    else:
        form = TransferForm()

    return render(request, 'transactions/transfer.html', {'form': form})


@login_required
def transaction_success(request, tracking_code):
    transaction = get_object_or_404(
        Transaction, tracking_code=tracking_code, user=request.user, status='success'
    )
    return render(request, 'transactions/success.html', {'transaction': transaction})


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)[:50]
    return render(request, 'transactions/history.html', {'transactions': transactions})


@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    return render(request, 'transactions/detail.html', {'transaction': transaction})
