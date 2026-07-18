import random
import uuid
from decimal import Decimal, InvalidOperation

from django.db import transaction

from .models import BankAccount, BankTransaction


class BankAPI:
    """API شبیه‌سازی شده بانک (برای تست/توسعه، نه اتصال به بانک واقعی)."""

    def __init__(self):
        self.FEE = Decimal(5000)
        self.MIN_AMOUNT = Decimal(10000)
        self.MAX_AMOUNT = Decimal(50000000)

    def check_balance(self, card_number):
        """بررسی موجودی کارت"""
        try:
            account = BankAccount.objects.get(card_number=card_number, is_active=True)
            return {
                'success': True,
                'balance': account.balance,
                'card_number': card_number,
            }
        except BankAccount.DoesNotExist:
            return {
                'success': False,
                'error': 'شماره کارت نامعتبر است',
            }

    def transfer(self, source_card, destination_card, amount, tracking_code=None):
        """انجام انتقال وجه بین دو کارت"""
        try:
            amount = Decimal(str(amount))
        except (InvalidOperation, TypeError, ValueError):
            return {'success': False, 'error': 'مبلغ نامعتبر است'}

        if source_card == destination_card:
            return {
                'success': False,
                'error': 'کارت مبدأ و مقصد نمی‌توانند یکسان باشند',
            }

        if amount < self.MIN_AMOUNT:
            return {
                'success': False,
                'error': f'حداقل مبلغ {self.MIN_AMOUNT:,} ریال است',
            }

        if amount > self.MAX_AMOUNT:
            return {
                'success': False,
                'error': f'حداکثر مبلغ {self.MAX_AMOUNT:,} ریال است',
            }

        try:
            with transaction.atomic():
                # قفل کردن هر دو حساب طبق ترتیب ثابت (بر اساس شماره کارت) تا از
                # deadlock بین تراکنش‌های هم‌زمان معکوس جلوگیری شود
                cards_in_order = sorted([source_card, destination_card])
                locked_accounts = {
                    acc.card_number: acc
                    for acc in BankAccount.objects
                    .select_for_update()
                    .filter(card_number__in=cards_in_order, is_active=True)
                }

                source_account = locked_accounts.get(source_card)
                if source_account is None:
                    return {'success': False, 'error': 'شماره کارت مبدأ نامعتبر است'}

                dest_account = locked_accounts.get(destination_card)
                if dest_account is None:
                    return {'success': False, 'error': 'شماره کارت مقصد نامعتبر است'}

                total_amount = amount + self.FEE

                if source_account.balance < total_amount:
                    return {
                        'success': False,
                        'error': f'موجودی کافی نیست. موجودی: {source_account.balance:,} ریال',
                    }

                if not tracking_code:
                    tracking_code = str(uuid.uuid4()).replace('-', '')[:20]

                reference_id = f"REF{random.randint(100000, 999999)}"

                source_account.balance -= total_amount
                source_account.save()

                dest_account.balance += amount
                dest_account.save()

                BankTransaction.objects.create(
                    tracking_code=tracking_code,
                    source_card=source_card,
                    destination_card=destination_card,
                    amount=amount,
                    fee=self.FEE,
                    status='success',
                    reference_id=reference_id,
                )

                return {
                    'success': True,
                    'reference_id': reference_id,
                    'tracking_code': tracking_code,
                    'source_balance': source_account.balance,
                    'dest_balance': dest_account.balance,
                    'fee': self.FEE,
                    'total_amount': total_amount,
                }

        except Exception as e:
            return {
                'success': False,
                'error': f'خطا در انجام تراکنش: {str(e)}',
            }

    def get_transaction(self, tracking_code):
        """دریافت اطلاعات یک تراکنش"""
        try:
            bank_transaction = BankTransaction.objects.get(tracking_code=tracking_code)
            return {
                'success': True,
                'data': {
                    'tracking_code': bank_transaction.tracking_code,
                    'source_card': bank_transaction.source_card,
                    'destination_card': bank_transaction.destination_card,
                    'amount': bank_transaction.amount,
                    'fee': bank_transaction.fee,
                    'status': bank_transaction.status,
                    'reference_id': bank_transaction.reference_id,
                    'created_at': bank_transaction.created_at,
                },
            }
        except BankTransaction.DoesNotExist:
            return {
                'success': False,
                'error': 'تراکنش یافت نشد',
            }

    def create_account(self, card_number, initial_balance=0, user=None):
        """ایجاد حساب بانکی جدید (برای تست)"""
        if BankAccount.objects.filter(card_number=card_number).exists():
            return {
                'success': False,
                'error': 'این شماره کارت قبلاً ثبت شده است',
            }
        try:
            account = BankAccount.objects.create(
                card_number=card_number,
                balance=initial_balance,
                is_active=True,
                user=user,
            )
            return {
                'success': True,
                'message': f'حساب با شماره {card_number} ایجاد شد',
                'data': {
                    'card_number': account.card_number,
                    'balance': account.balance,
                },
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'خطا در ایجاد حساب: {str(e)}',
            }

    def activate_account(self, card_number):
        """فعال/غیرفعال کردن حساب"""
        try:
            account = BankAccount.objects.get(card_number=card_number)
            account.is_active = not account.is_active
            account.save()
            status = 'فعال' if account.is_active else 'غیرفعال'
            return {
                'success': True,
                'message': f'حساب {status} شد',
            }
        except BankAccount.DoesNotExist:
            return {
                'success': False,
                'error': 'شماره کارت یافت نشد',
            }
