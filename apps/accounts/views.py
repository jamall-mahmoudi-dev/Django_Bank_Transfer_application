from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.backends import ModelBackend
from .forms import UserRegistrationForm, UserProfileForm
from .models import User

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'ثبت نام با موفقیت انجام شد!')
            return redirect('dashboard:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'خوش آمدید {user.username}!')
            
            # ========== مهم: اینجا همیشه به داشبورد برو ==========
            return redirect('dashboard:home')
            # ==================================================
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
@require_POST
def user_logout(request):
    # خروج فقط با POST مجاز است (استاندارد جنگو ۴.۱+)، تا یک لینک/عکس
    # مخرب خارجی نتونه صرفاً با GET کاربر رو لاگ‌اوت کنه
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('accounts:login')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل با موفقیت به‌روزرسانی شد!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'خطا در تغییر رمز عبور. لطفاً دوباره تلاش کنید.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})