from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User

class UserRegistrationForm(UserCreationForm):
    # اعتبارسنجی شماره تلفن
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message='شماره تلفن باید با 09 شروع شود و 11 رقم باشد'
    )
    
    phone_number = forms.CharField(
        max_length=11,
        required=True,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'placeholder': 'مثلاً 09123456789',
            'dir': 'ltr'
        }),
        label='شماره تلفن'
    )
    
    # اضافه کردن فیلد شماره کارت برای ثبت‌نام
    card_number = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'placeholder': 'شماره ۱۶ رقمی کارت',
            'maxlength': '16',
            'dir': 'ltr'
        }),
        label='شماره کارت',
        help_text='اختیاری - می‌توانید بعداً در پروفایل ثبت کنید'
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'placeholder': 'نام کاربری'
        }),
        label='نام کاربری',
        help_text=''  # حذف توضیحات
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'placeholder': 'example@email.com',
            'dir': 'ltr'
        }),
        label='ایمیل'
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'placeholder': 'رمز عبور'
        }),
        label='رمز عبور',
        help_text='رمز عبور باید حداقل ۸ کاراکتر باشد'  # توضیح خلاصه
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'placeholder': 'تکرار رمز عبور'
        }),
        label='تکرار رمز عبور',
        help_text=''  # حذف توضیحات
    )
    
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'card_number', 'password1', 'password2')
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # حذف فاصله و کاراکترهای اضافی
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        # بررسی اینکه شماره با 09 شروع شود
        if not phone_number.startswith('09'):
            raise forms.ValidationError('شماره تلفن باید با 09 شروع شود')
        
        # بررسی طول شماره
        if len(phone_number) != 11:
            raise forms.ValidationError('شماره تلفن باید 11 رقم باشد')
        
        # بررسی اینکه شماره تکراری نباشد
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('این شماره تلفن قبلاً ثبت شده است')
        
        return phone_number
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('این نام کاربری قبلاً ثبت شده است')
        return username
    
    def clean_card_number(self):
        card = self.cleaned_data.get('card_number')
        if card:
            card = card.strip().replace(' ', '').replace('-', '')
            if not card.isdigit():
                raise forms.ValidationError('شماره کارت باید فقط شامل اعداد باشد')
            if len(card) != 16:
                raise forms.ValidationError('شماره کارت باید ۱۶ رقم باشد')
        return card
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        user.card_number = self.cleaned_data.get('card_number', '')
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message='شماره تلفن باید با 09 شروع شود و 11 رقم باشد'
    )
    
    phone_number = forms.CharField(
        max_length=11,
        required=True,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'dir': 'ltr'
        }),
        label='شماره تلفن'
    )
    
    # اضافه کردن فیلد شماره کارت به فرم پروفایل
    card_number = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'placeholder': 'شماره ۱۶ رقمی کارت',
            'maxlength': '16',
            'dir': 'ltr'
        }),
        label='شماره کارت',
        help_text='شماره کارت ۱۶ رقمی خود را وارد کنید'
    )
    
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'placeholder': 'نام'
        }),
        label='نام'
    )
    
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'placeholder': 'نام خانوادگی'
        }),
        label='نام  خانوادگی'
    )
     
     
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:border-blue-500',
            'dir': 'ltr',
            'placeholder': 'example@email.com'
        }),
        label='ایمیل'
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'card_number')  # card_number را اضافه کنید
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        if not phone_number.startswith('09'):
            raise forms.ValidationError('شماره تلفن باید با 09 شروع شود')
        
        if len(phone_number) != 11:
            raise forms.ValidationError('شماره تلفن باید 11 رقم باشد')
        
        # بررسی اینکه شماره برای کاربر دیگر ثبت نشده باشد
        if User.objects.exclude(pk=self.instance.pk).filter(phone_number=phone_number).exists():
            raise forms.ValidationError('این شماره تلفن قبلاً ثبت شده است')
        
        return phone_number
    
    def clean_card_number(self):
        card = self.cleaned_data.get('card_number')
        if card:
            card = card.strip().replace(' ', '').replace('-', '')
            if not card.isdigit():
                raise forms.ValidationError('شماره کارت باید فقط شامل اعداد باشد')
            if len(card) != 16:
                raise forms.ValidationError('شماره کارت باید ۱۶ رقم باشد')
        return card