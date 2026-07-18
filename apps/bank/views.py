import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .api import BankAPI

bank_api = BankAPI()


@login_required
def test_bank_api(request):
    """صفحه تست API بانک"""
    return render(request, 'bank/test_api.html')


def _parse_json_body(request):
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError:
        return None, JsonResponse({'error': 'بدنه درخواست باید JSON معتبر باشد'}, status=400)


# نکته: csrf_exempt فقط برای درگاه فیک/تست قابل قبول است. این endpoint ها هنوز
# login_required هستند تا حداقل فقط کاربران واردشده بتوانند صدا بزنند.
# در محیط واقعی، به‌جای csrf_exempt از CSRF token در فرانت‌اند استفاده کنید.

@csrf_exempt
@login_required
@require_POST
def api_check_balance(request):
    """API بررسی موجودی"""
    data, error_response = _parse_json_body(request)
    if error_response:
        return error_response

    card_number = data.get('card_number')
    if not card_number:
        return JsonResponse({'error': 'شماره کارت الزامی است'}, status=400)

    result = bank_api.check_balance(card_number)
    if not result['success']:
        return JsonResponse(result, status=404)
    result['balance'] = int(result['balance'])
    return JsonResponse(result)


@csrf_exempt
@login_required
@require_POST
def api_transfer(request):
    """API انتقال وجه"""
    data, error_response = _parse_json_body(request)
    if error_response:
        return error_response

    source_card = data.get('source_card')
    destination_card = data.get('destination_card')
    amount = data.get('amount')

    if not source_card or not destination_card or amount is None:
        return JsonResponse({'error': 'اطلاعات ناقص است'}, status=400)

    result = bank_api.transfer(source_card, destination_card, amount)
    if not result['success']:
        return JsonResponse(result, status=400)

    result['source_balance'] = int(result['source_balance'])
    result['dest_balance'] = int(result['dest_balance'])
    result['fee'] = int(result['fee'])
    result['total_amount'] = int(result['total_amount'])
    result['message'] = 'انتقال با موفقیت انجام شد'
    return JsonResponse(result)


@csrf_exempt
@login_required
@require_POST
def api_create_account(request):
    """API ایجاد حساب بانکی"""
    data, error_response = _parse_json_body(request)
    if error_response:
        return error_response

    card_number = data.get('card_number')
    initial_balance = data.get('initial_balance', 0)

    if not card_number:
        return JsonResponse({'error': 'شماره کارت الزامی است'}, status=400)

    try:
        initial_balance = int(initial_balance)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'موجودی اولیه نامعتبر است'}, status=400)

    result = bank_api.create_account(card_number, initial_balance)
    if not result['success']:
        return JsonResponse(result, status=400)
    return JsonResponse(result)
