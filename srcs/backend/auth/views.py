import io
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import get_user_model
from django.conf import settings
from .models import CustomUser, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
import pyotp
import qrcode

CustomUser = get_user_model()

def verify_2fa_otp(user , otp ):
    totp = pyotp.TOTP(user.mfa_secret)
    if totp.verify(otp):
        user.mfa_enabled = True
        user.save()
        return True
    return False

def verify_mfa(request):
    if request.method == 'POST':
        otp = request.POST.get('otp_code')
        user_id = request.POST.get('user_id')
        if not user_id:
            messages.error(request, 'Invalid user id. Please try again.')
            return render(request,'otp_verify.html', {'user_id': user_id})
        
        user = CustomUser.objects.get(id=user_id)
        if verify_2fa_otp(user, otp):
            if request.user.is_authenticated:
                messages.success(request, '2FA enabled successfully !')
                return redirect('profile')

            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('profile')
        else:
            if request.user.is_authenticated:
                messages.error(request, 'Invalid OTP code. Please try again.')
                return redirect('profile')
            messages.error(request, 'Invalid OTP code. Please try again.')
            return render(request,'otp_verify.html', {'user_id': user_id})
       
    return render(request,'otp_verify.html', {'user_id': user_id})

@login_required
def disable_2fa(request):
    user = request.user
    if user.mfa_enabled:
        user.mfa_enabled = False
        user.save()
        messages.success(request, "Two-Factor Authentication has been disabled.")
        return redirect('profile')
    else:
        messages.info(request, "2FA is already disabled.")
    return redirect('profile')
