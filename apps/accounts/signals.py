import logging

from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

# مسیر import را متناسب با ساختار واقعی پروژه تنظیم کنید (طبق apps/bank/apps.py فعلی apps.bank است)
try:
    from apps.bank.models import BankAccount
except ImportError:
    from bank.models import BankAccount

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def sync_bank_account(sender, instance, created, **kwargs):
    """
    بدون این signal، کاربر تازه ثبت‌نام‌شده هیچ BankAccount ای در اپ bank
    نداره، و اولین انتقال وجهش همیشه با خطای «شماره کارت نامعتبر است»
    شکست می‌خوره - چون transactions.views از apps.bank.api.BankAPI استفاده
    می‌کنه که فقط روی جدول BankAccount کار می‌کنه، نه فیلد User.card_number.
    این signal هر بار که User ذخیره می‌شه و card_number داره، حساب متناظرش
    رو در بانک فیک می‌سازه یا شماره کارتش رو به‌روز می‌کنه.
    """
    if not instance.card_number:
        return

    try:
        with transaction.atomic():
            account, made = BankAccount.objects.get_or_create(
                user=instance,
                defaults={'card_number': instance.card_number, 'is_active': True},
            )
            if not made and account.card_number != instance.card_number:
                account.card_number = instance.card_number
                account.save(update_fields=['card_number'])
    except IntegrityError:
        # معمولاً یعنی این شماره کارت قبلاً برای یک BankAccount دیگر ثبت شده
        logger.warning(
            "sync_bank_account: could not sync BankAccount for user %s "
            "(card_number=%s) - likely a duplicate card number.",
            instance.pk, instance.card_number,
        )
