from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import BankAccount, BankTransaction
import uuid
import random

@login_required
def test_bank_api(request):
    """صفحه تست API بانک"""
    return render(request, 'bank/test_api.html')


@csrf_exempt
@login_required
def api_check_balance(request):
    """API بررسی موجودی - ساده شده"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        card_number = data.get('card_number')
        
        if not card_number:
            return JsonResponse({'error': 'شماره کارت الزامی است'}, status=400)
        
        # بررسی در دیتابیس
        try:
            account = BankAccount.objects.get(card_number=card_number)
            return JsonResponse({
                'success': True,
                'balance': int(account.balance),
                'card_number': card_number
            })
        except BankAccount.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'شماره کارت یافت نشد'
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@login_required
def api_transfer(request):
    """API انتقال وجه - ساده شده"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        source_card = data.get('source_card')
        destination_card = data.get('destination_card')
        amount = data.get('amount')
        
        if not source_card or not destination_card or not amount:
            return JsonResponse({'error': 'اطلاعات ناقص است'}, status=400)
        
        amount = int(amount)
        
        # اعتبارسنجی
        if amount < 10000:
            return JsonResponse({'error': 'حداقل مبلغ ۱۰,۰۰۰ ریال است'})
        
        if amount > 50000000:
            return JsonResponse({'error': 'حداکثر مبلغ ۵۰,۰۰۰,۰۰۰ ریال است'})
        
        # پیدا کردن حساب مبدأ
        try:
            source = BankAccount.objects.get(card_number=source_card)
        except BankAccount.DoesNotExist:
            return JsonResponse({'error': 'کارت مبدأ یافت نشد'})
        
        # پیدا کردن حساب مقصد
        try:
            dest = BankAccount.objects.get(card_number=destination_card)
        except BankAccount.DoesNotExist:
            return JsonResponse({'error': 'کارت مقصد یافت نشد'})
        
        # بررسی یکسان نبودن
        if source_card == destination_card:
            return JsonResponse({'error': 'کارت مبدأ و مقصد نمی‌توانند یکسان باشند'})
        
        # محاسبه کارمزد
        fee = 5000
        total = amount + fee
        
        # بررسی موجودی
        if source.balance < total:
            return JsonResponse({
                'error': f'موجودی کافی نیست. موجودی: {int(source.balance):,} ریال'
            })
        
        # انجام انتقال
        source.balance -= total
        source.save()
        
        dest.balance += amount
        dest.save()
        
        # تولید کد پیگیری
        tracking_code = str(uuid.uuid4()).replace('-', '')[:20]
        reference_id = f"REF{random.randint(100000, 999999)}"
        
        # ثبت تراکنش
        transaction = BankTransaction.objects.create(
            tracking_code=tracking_code,
            source_card=source_card,
            destination_card=destination_card,
            amount=amount,
            fee=fee,
            status='success',
            reference_id=reference_id
        )
        
        return JsonResponse({
            'success': True,
            'reference_id': reference_id,
            'tracking_code': tracking_code,
            'source_balance': int(source.balance),
            'dest_balance': int(dest.balance),
            'fee': fee,
            'total_amount': total,
            'message': f'انتقال با موفقیت انجام شد'
        })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@login_required
def api_create_account(request):
    """API ایجاد حساب بانکی"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        card_number = data.get('card_number')
        initial_balance = data.get('initial_balance', 0)
        
        if not card_number:
            return JsonResponse({'error': 'شماره کارت الزامی است'}, status=400)
        
        # بررسی وجود کارت
        if BankAccount.objects.filter(card_number=card_number).exists():
            return JsonResponse({'error': 'این شماره کارت قبلاً ثبت شده است'})
        
        # ایجاد حساب
        account = BankAccount.objects.create(
            card_number=card_number,
            balance=int(initial_balance),
            is_active=True
        )
        
        return JsonResponse({
            'success': True,
            'message': f'حساب با شماره {card_number} ایجاد شد',
            'data': {
                'card_number': account.card_number,
                'balance': int(account.balance)
            }
        })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)