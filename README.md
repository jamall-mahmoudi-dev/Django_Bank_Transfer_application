#  سیستم کارت به کارت (Card to Card Transfer System)

یک سیستم مدیریت انتقال وجه کارت به کارت با استفاده از  Django  و  Tailwind CSS  که امکان مدیریت تراکنش‌ها، موجودی و پروفایل کاربری را فراهم می‌کند.

##  ویژگی‌ها

-   سیستم احراز هویت کامل  (ثبت نام، ورود، خروج، تغییر رمز عبور)
-   مدیریت شماره کارت  در پروفایل کاربری
-  انتقال وجه  بین کارت‌ها با محاسبه کارمزد
-   داشبورد مدیریتی  با آمار و نمودارهای تراکنش
-   تاریخچه تراکنش‌ها  با نمایش جزئیات کامل
-   درگاه بانک فیک  برای تست و توسعه
-   طراحی واکنش‌گرا  (Responsive) برای موبایل و دسکتاپ
-   رابط کاربری زیبا  با Tailwind CSS و Font Awesome

##  تکنولوژی‌ها

-  Backend  Django 5.2.8
-  Frontend  Tailwind CSS, Font Awesome
-  Database  SQLite (قابل تغییر به PostgreSQL, MySQL)
-  Other  Django REST Framework, django-allauth

##  پیش‌نیازها

- Python 3.8 یا بالاتر
- pip (مدیریت بسته‌های Python)
- virtualenv (اختیاری)

##  نصب و راه‌اندازی

### ۱. کلون کردن پروژه

```bash
git clone https://github.com/yourusername/bank_transfer_app.git
cd bank_transfer_app
```

### ۲. ایجاد و فعال کردن محیط مجازی

```bash
# ویندوز
python -m venv venv
venv\Scripts\activate

# لینوکس / مک
python -m venv venv
source venv/bin/activate
```

### ۳. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### ۴. اجرای مایگریشن‌ها

```bash
python manage.py makemigrations
python manage.py migrate
```

### ۵. ایجاد کاربر ادمین (سوپرکاربر)

```bash
python manage.py createsuperuser
```

### ۶. ایجاد حساب‌های بانکی اولیه برای تست

```bash
python manage.py shell
```

```python
from apps.bank.models import BankAccount

# ایجاد حساب برای کاربر فعلی
BankAccount.objects.create(
    card_number='6037991234567890',  # شماره کارت خود را وارد کنید
    balance=10000000,
    is_active=True
)

# ایجاد حساب مقصد برای تست
BankAccount.objects.create(
    card_number='6037991111111111',
    balance=5000000,
    is_active=True
)
exit()
```

### ۷. اجرای سرور

```bash
python manage.py runserver 8000
```

### ۸. دسترسی به پروژه

-  وب‌سایت  `http://127.0.0.1:8000/`
-  پنل ادمین  `http://127.0.0.1:8000/admin/`
-  تست API بانک  `http://127.0.0.1:8000/bank/test/`

##  ساختار پروژه

```
bank_transfer_app/
├── apps/
│   ├── accounts/          # مدیریت کاربران
│   │   ├── models.py      # مدل User با فیلدهای اضافی
│   │   ├── views.py       # ثبت نام، ورود، پروفایل
│   │   ├── forms.py       # فرم‌های کاربری
│   │   └── urls.py        # مسیرهای accounts
│   ├── transactions/      # مدیریت تراکنش‌ها
│   │   ├── models.py      # مدل Transaction
│   │   ├── views.py       # انتقال، تاریخچه، جزئیات
│   │   ├── forms.py       # فرم انتقال
│   │   └── urls.py        # مسیرهای transactions
│   ├── dashboard/         # داشبورد کاربری
│   │   ├── views.py       # نمایش آمار و تراکنش‌ها
│   │   └── urls.py        # مسیرهای dashboard
│   └── bank/              # درگاه بانک فیک
│       ├── models.py      # مدل‌های بانکی
│       ├── api.py         # API شبیه‌سازی شده بانک
│       ├── views.py       # API endpoints
│       └── urls.py        # مسیرهای bank
├── config/                # تنظیمات پروژه
│   ├── settings.py
│   └── urls.py
├── templates/             # قالب‌های اصلی
│   └── base.html          # قالب پایه
├── static/                # فایل‌های استاتیک
├── manage.py
└── requirements.txt
```
 تنظیمات مهم

### مدل کاربر (User)

```python
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    balance = models.DecimalField(max_digits=15, decimal_places=0, default=0)
```

### تنظیمات لاگین

```python
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:home'
```

## 📱 صفحات پروژه

| صفحه | آدرس | توضیح |
|------|------|--------|
|  داشبورد  | `/` | نمایش آمار و آخرین تراکنش‌ها |
|  ورود  | `/accounts/login/` | ورود به سیستم |
|  ثبت نام  | `/accounts/register/` | ثبت نام کاربر جدید |
|  پروفایل  | `/accounts/profile/` | ویرایش اطلاعات کاربری |
|  انتقال وجه  | `/transactions/new/` | انجام انتقال وجه |
|  تاریخچه  | `/transactions/history/` | مشاهده تاریخچه تراکنش‌ها |
|  جزئیات تراکنش  | `/transactions/detail/<id>/` | مشاهده جزئیات تراکنش |
|  تست API بانک  | `/bank/test/` | تست API شبیه‌سازی شده بانک |

##  API های بانک

| آدرس | متد | توضیح |
|------|------|--------|
| `/bank/api/create-account/` | POST | ایجاد حساب بانکی جدید |
| `/bank/api/check-balance/` | POST | بررسی موجودی کارت |
| `/bank/api/transfer/` | POST | انتقال وجه بین کارت‌ها |

### نمونه درخواست انتقال وجه

```json
{
    "source_card": "6037991234567890",
    "destination_card": "6037991111111111",
    "amount": 100000
}
```

##  نکات توسعه

### اضافه کردن اپلیکیشن جدید

```bash
python manage.py startapp myapp
```

### اجرای تست‌ها

```bash
python manage.py test
```

### ایجاد مایگریشن جدید

```bash
python manage.py makemigrations
python manage.py migrate
```

### جمع‌آوری فایل‌های استاتیک

```bash
python manage.py collectstatic
```

##  مشارکت

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/AmazingFeature`)
3. Commit کنید (`git commit -m 'Add some AmazingFeature'`)
4. Push کنید (`git push origin feature/AmazingFeature`)
5. Pull Request باز کنید

##  پشتیبانی

-  ایمیل  jamallmahmoudi2001@gmail.com
-  تلگرام  @Bahram_mahoudi_523

##  مجوز

این پروژه تحت مجوز  MIT  منتشر شده است.

---

