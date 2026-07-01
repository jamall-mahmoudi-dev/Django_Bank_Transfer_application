import random
import hashlib
from datetime import datetime

class BankAPI:
    """API شبیه‌سازی شده برای بانک - با API واقعی جایگزین کنید"""
    
    def __init__(self):
        self.merchant_id = "TEST_MERCHANT_123"
    
    def check_balance(self, card_number):
        """بررسی موجودی کارت"""
        # شبیه‌سازی پاسخ بانک
        if card_number and len(card_number) == 16:
            # موجودی تصادفی بین 0 تا 10 میلیون
            balance = random.randint(0, 10000000)
            return {
                'success': True,
                'balance': balance,
                'card_number': card_number
            }
        return {
            'success': False,
            'error': 'شماره کارت نامعتبر است'
        }
    
    def transfer(self, source_card, destination_card, amount, tracking_code):
        """انجام انتقال پول"""
        # اعتبارسنجی ساده
        if not source_card or not destination_card:
            return {
                'success': False,
                'error': 'اطلاعات کارت کامل نیست'
            }
        
        if amount < 10000:
            return {
                'success': False,
                'error': 'مبلغ باید حداقل 10,000 ریال باشد'
            }
        
        # شبیه‌سازی موفقیت 95% تراکنش‌ها
        is_successful = random.random() > 0.05
        
        if is_successful:
            reference_id = hashlib.md5(
                f"{source_card}{destination_card}{amount}{datetime.now()}".encode()
            ).hexdigest()[:20]
            
            return {
                'success': True,
                'reference_id': reference_id,
                'message': 'تراکنش با موفقیت انجام شد'
            }
        else:
            return {
                'success': False,
                'error': 'خطا در ارتباط با بانک، لطفاً مجدد تلاش کنید'
            }