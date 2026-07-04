import random
import uuid
from decimal import Decimal
from django.db import transaction
from .models import BankAccount, BankTransaction

class BankAPI:
    """API شبیه‌سازی شده بانک"""
    
    def __init__(self):
        # کارمزد ثابت برای هر تراکنش (ریال)
        self.FEE = 5000
        # حداقل و حداکثر مبلغ
        self.MIN_AMOUNT = 10000
        self.MAX_AMOUNT = 50000000
    
    def check_balance(self, card_number):
        """
        بررسی موجودی کارت
        """
        try:
            account = BankAccount.objects.get(card_number=card_number, is_active=True)
            return {
                'success': True,
                'balance': account.balance,
                'card_number': card_number
            }
        except BankAccount.DoesNotExist:
            return {
                'success': False,
                'error': 'شماره کارت نامعتبر است'
            }
    
    def transfer(self, source_card, destination_card, amount, tracking_code=None):
        """
        انجام انتقال وجه بین دو کارت
        """
        try:
            with transaction.atomic():
                # اعتبارسنجی مبلغ
                if amount < self.MIN_AMOUNT:
                    return {
                        'success': False,
                        'error': f'حداقل مبلغ {self.MIN_AMOUNT:,} ریال است'
                    }
                
                if amount > self.MAX_AMOUNT:
                    return {
                        'success': False,
                        'error': f'حداکثر مبلغ {self.MAX_AMOUNT:,} ریال است'
                    }
                
                # یافتن حساب مبدأ
                try:
                    source_account = BankAccount.objects.select_for_update().get(
                        card_number=source_card, 
                        is_active=True
                    )
                except BankAccount.DoesNotExist:
                    return {
                        'success': False,
                        'error': 'شماره کارت مبدأ نامعتبر است'
                    }
                
                # یافتن حساب مقصد
                try:
                    dest_account = BankAccount.objects.select_for_update().get(
                        card_number=destination_card, 
                        is_active=True
                    )
                except BankAccount.DoesNotExist:
                    return {
                        'success': False,
                        'error': 'شماره کارت مقصد نامعتبر است'
                    }
                
                # بررسی اینکه کارت مبدأ و مقصد یکی نباشند
                if source_card == destination_card:
                    return {
                        'success': False,
                        'error': 'کارت مبدأ و مقصد نمی‌توانند یکسان باشند'
                    }
                
                # محاسبه مبلغ کل (مبلغ + کارمزد)
                total_amount = amount + self.FEE
                
                # بررسی موجودی
                if source_account.balance < total_amount:
                    return {
                        'success': False,
                        'error': f'موجودی کافی نیست. موجودی: {source_account.balance:,} ریال'
                    }
                
                # تولید کد پیگیری
                if not tracking_code:
                    tracking_code = str(uuid.uuid4()).replace('-', '')[:20]
                
                # تولید کد مرجع بانک
                reference_id = f"REF{random.randint(100000, 999999)}"
                
                # انجام انتقال
                source_account.balance -= total_amount
                source_account.save()
                
                dest_account.balance += amount
                dest_account.save()
                
                # ثبت تراکنش بانکی
                bank_transaction = BankTransaction.objects.create(
                    tracking_code=tracking_code,
                    source_card=source_card,
                    destination_card=destination_card,
                    amount=amount,
                    fee=self.FEE,
                    status='success',
                    reference_id=reference_id
                )
                
                return {
                    'success': True,
                    'reference_id': reference_id,
                    'tracking_code': tracking_code,
                    'source_balance': source_account.balance,
                    'dest_balance': dest_account.balance,
                    'fee': self.FEE,
                    'total_amount': total_amount
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'خطا در انجام تراکنش: {str(e)}'
            }
    
    def get_transaction(self, tracking_code):
        """
        دریافت اطلاعات یک تراکنش
        """
        try:
            transaction = BankTransaction.objects.get(tracking_code=tracking_code)
            return {
                'success': True,
                'data': {
                    'tracking_code': transaction.tracking_code,
                    'source_card': transaction.source_card,
                    'destination_card': transaction.destination_card,
                    'amount': transaction.amount,
                    'fee': transaction.fee,
                    'status': transaction.status,
                    'reference_id': transaction.reference_id,
                    'created_at': transaction.created_at
                }
            }
        except BankTransaction.DoesNotExist:
            return {
                'success': False,
                'error': 'تراکنش یافت نشد'
            }
    
    def create_account(self, card_number, initial_balance=0):
        """
        ایجاد حساب بانکی جدید (برای تست)
        """
        try:
            account = BankAccount.objects.create(
                card_number=card_number,
                balance=initial_balance,
                is_active=True
            )
            return {
                'success': True,
                'message': f'حساب با شماره {card_number} ایجاد شد',
                'data': {
                    'card_number': account.card_number,
                    'balance': account.balance
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'خطا در ایجاد حساب: {str(e)}'
            }
    
    def activate_account(self, card_number):
        """
        فعال/غیرفعال کردن حساب
        """
        try:
            account = BankAccount.objects.get(card_number=card_number)
            account.is_active = not account.is_active
            account.save()
            status = 'فعال' if account.is_active else 'غیرفعال'
            return {
                'success': True,
                'message': f'حساب {status} شد'
            }
        except BankAccount.DoesNotExist:
            return {
                'success': False,
                'error': 'شماره کارت یافت نشد'
            }